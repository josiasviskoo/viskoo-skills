#!/usr/bin/env python3
"""Monta a prévia das imagens geradas: carrossel deslizável com moldura do Instagram,
folha de contato (para revisão rápida) e, opcionalmente, PDF para o LinkedIn.

Uso:
    python3 montar_previa.py pasta_do_projeto [--handle @marca] [--legenda "…"] [--pdf]

Lê pasta/slides/slide_*.png (ou pasta/variante-*/slides/ em planos com variantes) e cria:
    pasta/previa.html     abra no navegador (arraste ou use as setas)
    pasta/folha.png       todos os slides lado a lado (o Claude lê esta imagem para revisar)
    pasta/carrossel.pdf   com --pdf
    pasta/folha-variantes.png   (planos com variantes) comparação lado a lado
Se existir plano.json, handle e legenda são lidos dele.
"""
import argparse
import html
import json
import sys
from pathlib import Path

PAGINA = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prévia do carrossel</title>
<style>
:root{--w:420px}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#e9e9ec;font-family:system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;gap:16px;padding:32px 16px;min-height:100vh}
.ig-frame{width:min(var(--w),100%);background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.12);overflow:hidden}
.ig-header{display:flex;align-items:center;gap:10px;padding:12px 14px}
.ig-avatar{width:32px;height:32px;border-radius:50%;background:#222;color:#fff;display:grid;place-items:center;font-weight:700;font-size:14px}
.ig-handle{font-size:13px;font-weight:600}.ig-sub{font-size:11px;color:#777}
.vp{overflow:hidden;aspect-ratio:__RATIO__;cursor:grab;touch-action:pan-y;user-select:none}
.track{display:flex;height:100%;transition:transform .35s ease}
.track img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;pointer-events:none}
.dots{display:flex;justify-content:center;gap:4px;padding:10px 0 2px}
.dots span{width:6px;height:6px;border-radius:50%;background:#d0d0d0}.dots span.on{background:#0095f6}
.cap{padding:10px 14px 14px;font-size:13px;line-height:1.45;white-space:pre-wrap}
.cap b{font-weight:600}
.dica{font-size:12px;color:#666}
</style></head><body>
<div class="ig-frame">
  <div class="ig-header"><div class="ig-avatar">__INICIAL__</div><div><div class="ig-handle">__HANDLE__</div><div class="ig-sub">Prévia</div></div></div>
  <div class="vp"><div class="track">__IMGS__</div></div>
  <div class="dots">__DOTS__</div>
  <div class="cap"><b>__HANDLE__</b> __LEGENDA__</div>
</div>
<p class="dica">Arraste ou use ← → · __N__ slides</p>
<script>
const t=document.querySelector('.track'),d=[...document.querySelectorAll('.dots span')],n=d.length;let a=0;
function ir(i){a=Math.max(0,Math.min(n-1,i));t.style.transform='translateX('+(-a*100)+'%)';d.forEach((e,j)=>e.classList.toggle('on',j===a));}
ir(0);const vp=document.querySelector('.vp');let x=null;
vp.addEventListener('pointerdown',e=>{x=e.clientX;vp.setPointerCapture(e.pointerId)});
vp.addEventListener('pointerup',e=>{if(x===null)return;const dx=e.clientX-x;x=null;if(Math.abs(dx)>40)ir(a+(dx<0?1:-1))});
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')ir(a+1);if(e.key==='ArrowLeft')ir(a-1)});
</script></body></html>"""


def folha_contato(imgs: list[Path], destino: Path, rotulos: list[str] | None = None) -> None:
    """Miniaturas lado a lado, cada uma preservando a própria proporção (formatos mistos ok)."""
    from PIL import Image, ImageDraw
    caixa, gap, cols = 360, 12, min(4, len(imgs))
    linhas = -(-len(imgs) // cols)
    alt_rot = 22 if rotulos else 0
    folha = Image.new("RGB", (cols * caixa + (cols + 1) * gap,
                              linhas * (caixa + alt_rot) + (linhas + 1) * gap), "#e9e9ec")
    d = ImageDraw.Draw(folha)
    for i, p in enumerate(imgs):
        im = Image.open(p).convert("RGB")
        im.thumbnail((caixa, caixa), Image.LANCZOS)
        x0 = gap + (i % cols) * (caixa + gap)
        y0 = gap + (i // cols) * (caixa + alt_rot + gap)
        if rotulos:
            d.text((x0, y0 + 4), rotulos[i], fill="#333")
        folha.paste(im, (x0 + (caixa - im.width) // 2, y0 + alt_rot + (caixa - im.height) // 2))
    folha.save(destino)


def montar(pasta: Path, handle: str | None, legenda: str | None, pdf: bool) -> list[Path]:
    from PIL import Image
    imgs = sorted((pasta / "slides").glob("slide_*.png"))
    if not imgs:
        return []
    plano = {}
    for cand in (pasta / "plano.json", pasta.parent / "plano.json"):
        if cand.exists():
            plano = json.loads(cand.read_text(encoding="utf-8"))
            break
    handle = (handle or plano.get("marca", {}).get("handle") or "suamarca").lstrip("@")
    legenda = legenda or plano.get("legenda", "")

    w, h = Image.open(imgs[0]).size
    pagina = (PAGINA.replace("__RATIO__", f"{w}/{h}")
              .replace("__IMGS__", "".join(f'<img src="slides/{p.name}" alt="Slide {i}">'
                                           for i, p in enumerate(imgs, 1)))
              .replace("__DOTS__", "<span></span>" * len(imgs))
              .replace("__HANDLE__", html.escape(handle))
              .replace("__INICIAL__", html.escape(handle[:1].upper()))
              .replace("__LEGENDA__", html.escape(legenda))
              .replace("__N__", str(len(imgs))))
    (pasta / "previa.html").write_text(pagina, encoding="utf-8")
    folha_contato(imgs, pasta / "folha.png")
    print(f"Prévia → {pasta / 'previa.html'}")
    print(f"Folha de contato → {pasta / 'folha.png'}")
    if pdf:
        paginas = [Image.open(p).convert("RGB") for p in imgs]
        paginas[0].save(pasta / "carrossel.pdf", save_all=True, append_images=paginas[1:])
        print(f"PDF → {pasta / 'carrossel.pdf'}")
    return imgs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta", type=Path)
    ap.add_argument("--handle")
    ap.add_argument("--legenda")
    ap.add_argument("--pdf", action="store_true", help="gera carrossel.pdf (LinkedIn)")
    a = ap.parse_args()
    try:
        import PIL  # noqa: F401
    except ImportError:
        sys.exit("Pillow não instalado: pip install pillow")

    pasta = a.pasta.resolve()
    if montar(pasta, a.handle, a.legenda, a.pdf):
        return
    # plano com variantes: uma prévia por variante + folha comparativa
    todas, rotulos = [], []
    for sub in sorted(pasta.glob("variante-*")):
        imgs = montar(sub, a.handle, a.legenda, a.pdf)
        todas += imgs
        rotulos += [f"{sub.name.replace('variante-', 'Variante ')} · {p.stem}" for p in imgs]
    if not todas:
        sys.exit(f"Nenhum slide em {pasta / 'slides'} nem em {pasta}/variante-*/slides")
    folha_contato(todas, pasta / "folha-variantes.png", rotulos)
    print(f"Comparação das variantes → {pasta / 'folha-variantes.png'}")


if __name__ == "__main__":
    main()

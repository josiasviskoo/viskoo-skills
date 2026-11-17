#!/usr/bin/env python3
"""Gera as imagens finais das peças de um plano.json usando o Codex CLI (ChatGPT).

O Claude escreve o plano (copy, estilo, layout por slide); este script monta um
prompt estruturado por slide, chama `codex exec` (ferramenta interna image_gen,
login do ChatGPT, sem chave de API) e ajusta cada imagem ao tamanho exato da rede.

Uso:
    python3 gerar_com_codex.py plano.json                    # gera tudo
    python3 gerar_com_codex.py plano.json --prompts          # só mostra os prompts (sem gastar)
    python3 gerar_com_codex.py plano.json --slides 2,5       # (re)gera só alguns
    python3 gerar_com_codex.py plano.json --ajustar 3 --instrucao "troque o título por ..."
    python3 gerar_com_codex.py plano.json -j 3               # 3 gerações em paralelo
    python3 gerar_com_codex.py plano.json --variante B       # só a variante B (planos com "variantes")

Modos (campo "modo" do plano): "carrossel" (padrão com >1 peça: barra, seta, slide 1 como
referência de estilo), "anuncio" (lote de criativos independentes, cada um com ângulo e design
próprios) e "post" (peça única). "variantes": {"A": {...}, "B": {...}} gera o mesmo conteúdo em
designs totalmente diferentes, cada variante em <pasta>/variante-X/.

Saída (ao lado do plano.json, ou em "pasta" do plano):
    bruto/slide_01.png      imagem original do Codex (versões antigas: slide_01_v1.png …)
    slides/slide_01.png     final no tamanho exato (ex.: 1080×1350)
    prompts/slide_01.txt    prompt enviado
    logs/slide_01.jsonl     eventos do Codex

Requer: codex CLI logado (`codex login`) e Pillow (`pip install pillow`).
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# formato -> (tamanho final exato, tamanho pedido ao Codex [múltiplos de 16], descrição)
FORMATOS = {
    "4:5":    ((1080, 1350), (1088, 1360), "portrait 4:5"),
    "1:1":    ((1080, 1080), (1088, 1088), "square 1:1"),
    "9:16":   ((1080, 1920), (1152, 2048), "vertical 9:16"),
    "16:9":   ((1200, 675),  (1536, 864),  "landscape 16:9"),
    "yt":     ((1280, 720),  (1536, 864),  "landscape 16:9 (YouTube thumbnail)"),
    "1.91:1": ((1200, 627),  (1536, 800),  "wide landscape ~1.91:1"),
    "2:3":    ((1000, 1500), (1024, 1536), "portrait 2:3"),
}

CODEX_IMG_DIR = Path.home() / ".codex" / "generated_images"


# ---------------------------------------------------------------- prompt
def _texto_verbatim(textos: dict) -> str:
    ordem = ["marca", "tag", "titulo", "subtitulo", "corpo", "itens", "cta", "rodape"]
    nomes = {"marca": "Brand name (small, in the brand lockup)", "tag": "Small label / tag (keep the casing exactly as written)", "titulo": "Headline", "subtitulo": "Subheadline",
             "corpo": "Body text", "itens": "List items", "cta": "Button / CTA",
             "rodape": "Footer"}
    linhas = []
    for k in ordem + [k for k in textos if k not in ordem]:
        v = textos.get(k)
        if not v:
            continue
        if isinstance(v, list):
            itens = "; ".join(f'"{i}"' for i in v)
            linhas.append(f"- {nomes.get(k, k)}: {itens}")
        else:
            linhas.append(f'- {nomes.get(k, k)}: "{v}"')
    return "\n".join(linhas)


def montar_prompt(plano: dict, s: dict, idx: int, total: int, refs: list[tuple[Path, str]]) -> str:
    fmt = s.get("formato", plano.get("formato", "4:5"))
    (fw, fh), (gw, gh), desc = FORMATOS[fmt]
    marca = plano.get("marca", {})
    cores = marca.get("cores", {})
    fontes = marca.get("fontes", {})
    modo = plano.get("modo", "carrossel" if total > 1 else "post")
    tipo_peca = plano.get("tipo", {"anuncio": "Meta Ads static creative",
                                   "post": "Instagram feed post"}.get(modo, "Instagram carousel slide"))
    eh_carrossel = total > 1 and modo == "carrossel"
    ui = s.get("ui", plano.get("ui", eh_carrossel))

    if "prompt" in s:  # prompt livre escrito pelo Claude
        corpo = s["prompt"].strip()
    else:
        partes = [
            f"Use case: {s.get('caso_de_uso', plano.get('caso_de_uso', 'ads-marketing'))}",
            f"Asset type: {tipo_peca}" + (f" {idx} of {total}" if total > 1 else "")
            + f", {desc}, final export {fw}x{fh}px",
            f"Primary request: {s.get('objetivo', s.get('tipo', 'social media post'))}",
        ]
        if modo == "anuncio" and total > 1:
            partes.append(f"Batch note: creative {idx} of {total} for the same offer. This one has its own "
                          "angle, image, headline and layout; it must not look like a copy of the others")
        if plano.get("_variante"):
            nome_v, desc_v, n_v = plano["_variante"]
            partes.append(f"Design variant {nome_v} of {n_v}: {desc_v}. All variants share exactly the same "
                          "text, but each must look completely different (layout, scene, framing, dominant "
                          "color, typography treatment)")
        if plano.get("estilo"):
            rotulo = "identical on every slide" if eh_carrossel else "brand look"
            partes.append(f"Style/medium ({rotulo}): {plano['estilo']}")
        if plano.get("layout_geral"):
            partes.append(f"Overall layout system: {plano['layout_geral']}")
        fundo = s.get("fundo")
        if fundo:
            partes.append(f"Scene/backdrop: {fundo}")
        if s.get("visual"):
            partes.append(f"Subject / main visual: {s['visual']}")
        if s.get("layout"):
            partes.append(f"Composition/framing: {s['layout']}")
        if cores:
            partes.append("Color palette (use these exact hex values): "
                          + ", ".join(f"{k} {v}" for k, v in cores.items()))
        if fontes:
            partes.append("Typography: " + ", ".join(f"{k}: {v}" for k, v in fontes.items())
                          + " (or the closest look-alike); clear hierarchy, generous spacing")
        textos = dict(s.get("textos", {}))
        if marca.get("nome") and s.get("mostrar_marca", idx in (1, total)):
            textos.setdefault("marca", marca["nome"])
        if textos:
            partes.append("Text (verbatim, Brazilian Portuguese, keep every accent and punctuation, "
                          "render each exactly once, no other words):\n" + _texto_verbatim(textos))
        if ui and eh_carrossel:
            pct = round(idx / total * 100)
            ui_txt = (f"Carousel UI baked into the image: a thin rounded progress bar along the bottom "
                      f"(about 3% of the height from the bottom edge, left and right margins equal), "
                      f"filled {pct}% from the left in the accent color, with a small counter "
                      f'"{idx}/{total}" to its right')
            if idx < total:
                ui_txt += "; a subtle chevron arrow ( > ) at the vertical middle of the right edge hinting to swipe"
            else:
                ui_txt += "; NO swipe arrow on this last slide"
            partes.append(ui_txt)
        restr = [
            "keep all text and key elements inside a safe margin of at least 6% from every edge "
            "(the image will be lightly cropped/resized)",
            "text must be crisp, high-contrast (WCAG AA) and readable at thumbnail size",
            "no watermark, no fake UI from Instagram itself, no extra logos, no lorem ipsum",
            "no em dashes or en dashes in any text",
            "icons only next to the information they illustrate, never loose decorative icons in corners",
            "do not invent numbers, prices, percentages or promises",
        ]
        if any(p.endswith("reference") or "reference" in p for _, p in refs):
            restr.append("from reference images take only the visual language; never copy their text, "
                         "logos, phone numbers, prices or people unless a reference explicitly says so")
        if plano.get("restricoes"):
            restr += plano["restricoes"]
        if s.get("restricoes"):
            restr += s["restricoes"]
        partes.append("Constraints: " + "; ".join(restr))
        evitar = plano.get("evitar", []) + s.get("evitar", [])
        if evitar:
            partes.append("Avoid: " + "; ".join(evitar))
        corpo = "\n".join(partes)

    if refs:
        linhas = [f"Image {i}: {papel}" for i, (_, papel) in enumerate(refs, 1)]
        corpo = "Input images:\n" + "\n".join(linhas) + "\n\n" + corpo
    return corpo


def instrucao_codex(prompt_imagem: str, destino: str, tamanho: tuple[int, int], edicao: bool) -> str:
    gw, gh = tamanho
    acao = ("Edit the attached image (Image 1 is the edit target) with your built-in image_gen tool"
            if edicao else "Generate ONE image with your built-in image_gen tool")
    return (
        f"{acao}, using the spec below. Request size {gw}x{gh} if the tool allows it; otherwise "
        f"the closest size with the same orientation.\n"
        f"Do not write code, SVG or HTML and do not use the CLI fallback.\n"
        f"Generate exactly one image (one image_gen call), then copy it to ./{destino} in the "
        f"current directory and reply only with that path.\n\n"
        f"=== IMAGE SPEC ===\n{prompt_imagem}\n=== END SPEC ==="
    )


# ---------------------------------------------------------------- execução
def _listar_geradas() -> set[Path]:
    return set(CODEX_IMG_DIR.rglob("*.png")) if CODEX_IMG_DIR.exists() else set()


def ajustar_tamanho(origem: Path, destino: Path, alvo: tuple[int, int]) -> tuple[int, int]:
    from PIL import Image
    img = Image.open(origem).convert("RGB")
    w, h = img.size
    aw, ah = alvo
    escala = max(aw / w, ah / h)
    nw, nh = round(w * escala), round(h * escala)
    img = img.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - aw) // 2, (nh - ah) // 2
    img.crop((x, y, x + aw, y + ah)).save(destino, "PNG", optimize=True)
    return w, h


def rodar_codex(instrucao: str, pasta: Path, imagens: list[Path], log: Path,
                modelo: str | None, timeout: int) -> None:
    cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "workspace-write",
           "-C", str(pasta), "--json", "--color", "never"]
    if modelo:
        cmd += ["-m", modelo]
    for img in imagens:
        cmd += ["-i", str(img)]
    # prompt via stdin (o -i aceita vários valores e engoliria o prompt posicional)
    with open(log, "w") as f:
        subprocess.run(cmd, input=instrucao, text=True, stdout=f, stderr=subprocess.STDOUT,
                       timeout=timeout, check=False)


def _ref(plano: dict, r, papel_padrao: str) -> tuple[Path, str]:
    raiz = Path(plano.get("_dir", "."))
    if isinstance(r, dict):
        return (raiz / r["arquivo"]).resolve(), r.get("papel", papel_padrao)
    return (raiz / r).resolve(), papel_padrao


def _avisos_texto(plano: dict) -> list[str]:
    avisos = []
    for i, s in enumerate(plano["slides"], 1):
        for k, v in s.get("textos", {}).items():
            for txt in (v if isinstance(v, list) else [v]):
                if "\u2014" in txt or "\u2013" in txt:
                    avisos.append(f"slide {i} ({k}): tem travessão: {txt!r}")
                if len(txt.split()) > 40:
                    avisos.append(f"slide {i} ({k}): {len(txt.split())} palavras; encurte (máx. ~40)")
    return avisos


def _mesclar(plano: dict, ov: dict) -> dict:
    novo = json.loads(json.dumps(plano))
    for k, v in ov.items():
        if k in ("referencias", "evitar", "restricoes"):
            novo[k] = plano.get(k, []) + v
        elif k == "marca":
            novo["marca"] = {**plano.get("marca", {}), **v}
        elif k == "slides":  # sobrescritas por slide: lista na mesma ordem
            for s, so in zip(novo["slides"], v):
                s.update(so or {})
        elif k != "descricao":
            novo[k] = v
    return novo


def gerar_um(plano: dict, base: Path, s: dict, idx: int, total: int, extra_refs: list[tuple[Path, str]],
             args, edicao_instr: str | None = None) -> str:
    nome = f"slide_{idx:02d}"
    fmt = s.get("formato", plano.get("formato", "4:5"))
    final, pedido, _ = FORMATOS[fmt]
    bruto, finais = base / "bruto", base / "slides"
    for d in (bruto, finais, base / "prompts", base / "logs"):
        d.mkdir(parents=True, exist_ok=True)

    refs: list[tuple[Path, str]] = []
    if edicao_instr:
        alvo = bruto / f"{nome}.png"
        if not alvo.exists():
            return f"{nome}: não há imagem para ajustar ({alvo})"
        refs.append((alvo, "edit target (current version of this slide)"))
    for r in s.get("referencias", []):
        refs.append(_ref(plano, r, "reference image"))
    refs += extra_refs
    faltando = [str(p) for p, _ in refs if not p.exists()]
    aviso = ""
    if faltando:
        if not args.prompts:
            return f"{nome}: ERRO, referência não encontrada: {', '.join(faltando)}"
        aviso = f"AVISO: referência não encontrada (a geração vai falhar): {', '.join(faltando)}\n"

    if edicao_instr:
        prompt = (
            "Use case: precise-object-edit\n"
            f"Primary request: {edicao_instr}\n"
            "Constraints: change ONLY what the request asks; keep layout, colors, typography, all other "
            "text (verbatim), progress bar, counter and arrow exactly as they are; same aspect ratio.\n\n"
            "Original spec of this slide, for context:\n" + montar_prompt(plano, s, idx, total, [])
        )
        prompt = "Input images:\n" + "\n".join(
            f"Image {i}: {p}" for i, (_, p) in enumerate(refs, 1)) + "\n\n" + prompt
    else:
        prompt = montar_prompt(plano, s, idx, total, refs)
    (base / "prompts" / f"{nome}.txt").write_text(prompt, encoding="utf-8")
    if args.prompts:
        return f"----- {nome} -----\n{aviso}{prompt}\n"

    destino_tmp = f"{nome}.novo.png"
    instr = instrucao_codex(prompt, destino_tmp, pedido, bool(edicao_instr))
    tentativas = 1 + args.tentativas
    for t in range(tentativas):
        antes = _listar_geradas()
        inicio = time.time()
        try:
            rodar_codex(instr, bruto, [p for p, _ in refs], base / "logs" / f"{nome}.jsonl",
                        args.modelo, args.timeout)
        except subprocess.TimeoutExpired:
            if t + 1 < tentativas:
                continue
            return f"{nome}: tempo esgotado ({args.timeout}s)"
        novo = bruto / destino_tmp
        if not novo.exists():  # plano B: pegar a imagem nova em ~/.codex/generated_images
            geradas = [p for p in _listar_geradas() - antes if p.stat().st_mtime >= inicio - 1]
            if geradas:
                shutil.copy2(max(geradas, key=lambda p: p.stat().st_mtime), novo)
        if novo.exists():
            atual = bruto / f"{nome}.png"
            if atual.exists():  # versiona a anterior
                v = 1
                while (bruto / f"{nome}_v{v}.png").exists():
                    v += 1
                atual.rename(bruto / f"{nome}_v{v}.png")
            novo.rename(atual)
            w, h = ajustar_tamanho(atual, finais / f"{nome}.png", final)
            seg = time.time() - inicio
            return f"{nome}: ok ({w}×{h} → {final[0]}×{final[1]}, {seg:.0f}s) → {finais / (nome + '.png')}"
    return f"{nome}: o Codex não gerou imagem; veja {base / 'logs' / (nome + '.jsonl')}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plano", type=Path)
    ap.add_argument("--slides", help="lista de números, ex.: 1,3,5 (padrão: todos)")
    ap.add_argument("--prompts", action="store_true", help="só grava e mostra os prompts; não chama o Codex")
    ap.add_argument("--ajustar", type=int, help="número do slide a editar a partir da versão atual")
    ap.add_argument("--instrucao", help="o que mudar (com --ajustar)")
    ap.add_argument("-j", "--paralelo", type=int, default=2, help="gerações simultâneas (padrão 2)")
    ap.add_argument("--sem-referencia-de-estilo", action="store_true",
                    help="não usar o slide 1 como referência visual para os demais")
    ap.add_argument("--variante", help="gera só esta variante (planos com \"variantes\")")
    ap.add_argument("--modelo", help="modelo do Codex (-m); padrão: o do config do Codex")
    ap.add_argument("--timeout", type=int, default=600, help="segundos por imagem (padrão 600)")
    ap.add_argument("--tentativas", type=int, default=1, help="novas tentativas em caso de falha (padrão 1)")
    args = ap.parse_args()

    plano = json.loads(args.plano.read_text(encoding="utf-8"))
    base = (args.plano.parent / plano.get("pasta", ".")).resolve()
    for f, s in enumerate(plano["slides"]):
        fmt = s.get("formato", plano.get("formato", "4:5"))
        if fmt not in FORMATOS:
            sys.exit(f"Formato inválido no slide {f + 1}: {fmt}. Use: {', '.join(FORMATOS)}")

    if not args.prompts:
        if not shutil.which("codex"):
            sys.exit("Codex CLI não encontrado. Instale: npm i -g @openai/codex  e rode: codex login")
        try:
            import PIL  # noqa: F401
        except ImportError:
            sys.exit("Pillow não instalado: pip install pillow")

    plano["_dir"] = str(args.plano.parent.resolve())
    for aviso in _avisos_texto(plano):
        print("AVISO:", aviso, file=sys.stderr)

    variantes = plano.get("variantes") or {}
    if args.variante:
        if args.variante not in variantes:
            sys.exit(f"Variante {args.variante!r} não existe no plano. Disponíveis: {', '.join(variantes) or 'nenhuma'}")
        variantes = {args.variante: variantes[args.variante]}
    if not variantes:
        processar(plano, base, args)
        return
    n_v = len(plano["variantes"])
    for nome_v, ov in variantes.items():
        pv = _mesclar(plano, ov)
        pv["_variante"] = (nome_v, ov.get("descricao", ""), n_v)
        print(f"=== Variante {nome_v} ===", flush=True)
        processar(pv, base / f"variante-{nome_v}", args)


def processar(plano: dict, base: Path, args) -> None:
    slides = plano["slides"]
    total = len(slides)
    globais = [_ref(plano, r, "brand reference") for r in plano.get("referencias", [])]

    if args.ajustar:
        if not args.instrucao:
            sys.exit("--ajustar exige --instrucao")
        i = args.ajustar
        print(gerar_um(plano, base, slides[i - 1], i, total, globais, args, args.instrucao))
        return

    alvo = [int(x) for x in args.slides.split(",")] if args.slides else list(range(1, total + 1))
    estilo_ref = base / "bruto" / "slide_01.png"
    modo = plano.get("modo", "carrossel" if total > 1 else "post")
    usar_ref = (total > 1 and modo == "carrossel" and not args.sem_referencia_de_estilo
                and not args.prompts)

    def refs_para(i: int):
        r = list(globais)
        if usar_ref and i != 1 and estilo_ref.exists():
            r.append((estilo_ref, "style reference: slide 1 of this same carousel. Match its palette, "
                      "typography, margins, grid, progress-bar style and overall look exactly. "
                      "Do NOT copy its text or main visual"))
        return r

    # slide 1 primeiro (vira referência de estilo), depois o resto em paralelo
    if 1 in alvo and usar_ref:
        print(gerar_um(plano, base, slides[0], 1, total, refs_para(1), args), flush=True)
        alvo = [i for i in alvo if i != 1]
    if args.prompts:
        for i in alvo:
            print(gerar_um(plano, base, slides[i - 1], i, total, refs_para(i), args))
        return
    with ThreadPoolExecutor(max_workers=max(1, args.paralelo)) as ex:
        futs = {ex.submit(gerar_um, plano, base, slides[i - 1], i, total, refs_para(i), args): i for i in alvo}
        for fut in as_completed(futs):
            print(fut.result(), flush=True)


if __name__ == "__main__":
    main()

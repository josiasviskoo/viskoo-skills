#!/usr/bin/env python3
"""Exporta cada slide de uma prévia de carrossel (assets/template-carrossel.html) para PNG.

Uso:
    python3 exportar_slides.py carrossel.html [--saida slides/] [--largura 1080] [--pdf]

O layout é renderizado na largura pequena do template (~420 px) e ampliado com
device_scale_factor, então a saída tem 1080 px de largura sem refluir o layout.

Requer: pip install playwright && python3 -m playwright install chromium
(--pdf requer Pillow: pip install pillow)
"""
import argparse
import asyncio
import sys
from pathlib import Path


async def exportar(html: Path, saida: Path, largura: int) -> list[Path]:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        sys.exit("Playwright não instalado. Rode: pip install playwright && python3 -m playwright install chromium")

    saida.mkdir(parents=True, exist_ok=True)
    arquivos = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # 1ª passada: descobrir dimensões do formato
        page = await browser.new_page()
        await page.goto(html.resolve().as_uri(), wait_until="networkidle")
        w, h = await page.evaluate("window.dimensoesSlide")
        await page.close()

        page = await browser.new_page(viewport={"width": w, "height": h},
                                      device_scale_factor=largura / w)
        await page.goto(html.resolve().as_uri(), wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(800)
        await page.evaluate("document.body.classList.add('exportando')")
        total = await page.evaluate("window.totalSlides")

        for i in range(total):
            await page.evaluate("i => window.irParaSlide(i)", i)
            await page.wait_for_timeout(150)
            vp = await page.query_selector(".carousel-viewport")
            caixa = await vp.bounding_box()
            destino = saida / f"slide_{i + 1:02d}.png"
            await page.screenshot(path=str(destino), clip={
                "x": caixa["x"], "y": caixa["y"], "width": w, "height": h})
            arquivos.append(destino)
            print(f"Slide {i + 1}/{total} → {destino}")
        await browser.close()
    return arquivos


def gerar_pdf(arquivos: list[Path], destino: Path) -> None:
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Para --pdf instale o Pillow: pip install pillow")
    imgs = [Image.open(a).convert("RGB") for a in arquivos]
    imgs[0].save(destino, save_all=True, append_images=imgs[1:])
    print(f"PDF (carrossel LinkedIn) → {destino}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path, help="arquivo HTML da prévia")
    ap.add_argument("--saida", type=Path, default=None, help="pasta dos PNGs (padrão: <pasta do html>/slides)")
    ap.add_argument("--largura", type=int, default=1080, help="largura final em px (padrão 1080)")
    ap.add_argument("--pdf", action="store_true", help="também gera carrossel.pdf (para LinkedIn)")
    a = ap.parse_args()
    if not a.html.exists():
        sys.exit(f"Arquivo não encontrado: {a.html}")
    saida = a.saida or a.html.parent / "slides"
    arquivos = asyncio.run(exportar(a.html, saida, a.largura))
    if a.pdf and arquivos:
        gerar_pdf(arquivos, saida / "carrossel.pdf")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Converte uma imagem em data: URI base64 para embutir no HTML do carrossel.

Uso:
    python3 embutir_imagem.py foto.jpg                 # imprime o data URI
    python3 embutir_imagem.py foto.jpg --max 1400      # reduz antes (requer Pillow)

Detecta o tipo real pelo conteúdo do arquivo (a extensão pode mentir).
Use o resultado em: <img class="bg" src="DATA_URI"> e insira no HTML via Python,
nunca via heredoc/echo no shell ($ e crases corrompem a string).
"""
import argparse
import base64
import io
import sys
from pathlib import Path

ASSINATURAS = [
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"GIF8", "image/gif"),
    (b"RIFF", "image/webp"),  # confirmado abaixo
    (b"<svg", "image/svg+xml"),
    (b"<?xml", "image/svg+xml"),
]


def detectar_mime(dados: bytes) -> str:
    for assinatura, mime in ASSINATURAS:
        if dados.startswith(assinatura):
            if mime == "image/webp" and dados[8:12] != b"WEBP":
                continue
            return mime
    sys.exit("Formato de imagem não reconhecido (use PNG, JPEG, GIF, WEBP ou SVG).")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("imagem", type=Path)
    ap.add_argument("--max", type=int, default=0, help="lado maior máximo em px (reduz tamanho do HTML)")
    a = ap.parse_args()

    dados = a.imagem.read_bytes()
    mime = detectar_mime(dados)

    if a.max and mime in ("image/png", "image/jpeg", "image/webp"):
        try:
            from PIL import Image
        except ImportError:
            sys.exit("--max requer Pillow: pip install pillow")
        img = Image.open(io.BytesIO(dados))
        img.thumbnail((a.max, a.max))
        buf = io.BytesIO()
        if mime == "image/png" and img.mode in ("RGBA", "LA", "P"):
            img.save(buf, "PNG", optimize=True)
        else:
            img.convert("RGB").save(buf, "JPEG", quality=85)
            mime = "image/jpeg"
        dados = buf.getvalue()

    kb = len(dados) / 1024
    if kb > 1500:
        print(f"Aviso: imagem com {kb:.0f} KB; considere --max 1400.", file=sys.stderr)
    print(f"data:{mime};base64,{base64.b64encode(dados).decode()}")


if __name__ == "__main__":
    main()

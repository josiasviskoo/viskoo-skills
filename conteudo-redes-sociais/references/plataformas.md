# Especificações por plataforma

Fonte da verdade para dimensões. Valores de 2025/2026; as redes mudam com
frequência, então confirme na documentação oficial se algo parecer diferente.

## Imagens e carrosséis

| Rede | Formato | Pixels | Proporção | Slides | Postura de design |
|---|---|---|---|---|---|
| Instagram | Carrossel (recomendado) | 1080×1350 | 4:5 | até 20 | uma ideia por card, continuidade visual |
| Instagram | Post quadrado | 1080×1080 | 1:1 | n/a | vibrante, alto contraste |
| Instagram | Story / capa de Reels | 1080×1920 | 9:16 | n/a | vertical, texto na zona segura |
| LinkedIn | Carrossel (documento/PDF) | 1080×1350 | 4:5 | até 20 | limpo, legível, foco em valor |
| LinkedIn | Post com imagem | 1200×627 ou 1080×1350 | 1.91:1 / 4:5 | n/a | profissional, crível |
| Twitter/X | Imagem de post | 1200×675 | 16:9 | até 4 | ousado, simples, impacto instantâneo |
| Twitter/X | Imagem quadrada | 1080×1080 | 1:1 | até 4 | n/a |
| Facebook | Carrossel / post | 1080×1080 | 1:1 ou 4:5 | até 10 | n/a |
| TikTok | Capa / arte | 1080×1920 | 9:16 | n/a | texto grande, energético, autêntico |
| YouTube | Thumbnail | 1280×720 | 16:9 | n/a | rosto/emoção, 3–5 palavras, contraste alto |
| YouTube | Shorts | 1080×1920 | 9:16 | n/a | n/a |
| Pinterest | Pin padrão | 1000×1500 | 2:3 | n/a | vertical, inspirador, alta qualidade |

**Carrossel no LinkedIn**: exporte os PNGs e junte num PDF (o LinkedIn exibe
PDF como carrossel). Exemplo:
`python3 -c "from PIL import Image; import glob; i=[Image.open(f).convert('RGB') for f in sorted(glob.glob('slides/*.png'))]; i[0].save('carrossel.pdf', save_all=True, append_images=i[1:])"`

## Vídeo

| Rede | Proporção | Duração típica | Resolução |
|---|---|---|---|
| TikTok | 9:16 | 15–60 s | 1080×1920 |
| Instagram Reels | 9:16 | 15–90 s | 1080×1920 |
| YouTube Shorts | 9:16 | < 60 s | 1080×1920 |
| Twitter/X | 16:9 ou 1:1 | < 140 s | 1920×1080 |

## Zonas seguras

- **Stories/Reels/TikTok (1080×1920)**: deixe ~250 px livres no topo e ~340 px
  embaixo (barra de perfil, legenda, botões). Texto importante no centro.
  À direita, evite ~120 px (botões de curtir/comentar).
- **Grade do perfil Instagram**: a miniatura do grid corta o 4:5 para 3:4.
  Mantenha o gancho do slide 1 no centro vertical.
- **Thumbnail YouTube**: o canto inferior direito tem o selo de duração.

## Formatos aceitos pelo `gerar_com_codex.py`

| `formato` | Pedido ao Codex | Final exato |
|---|---|---|
| `4:5` | 1088×1360 | 1080×1350 |
| `1:1` | 1088×1088 | 1080×1080 |
| `9:16` | 1152×2048 | 1080×1920 |
| `16:9` | 1536×864 | 1200×675 |
| `yt` | 1536×864 | 1280×720 |
| `1.91:1` | 1536×800 | 1200×627 |
| `2:3` | 1024×1536 | 1000×1500 |

O script redimensiona e recorta pelo centro. Por isso o prompt sempre pede
margem de segurança de 6% em todas as bordas.

Para stories/Reels/TikTok, acrescente a zona segura ao `layout` do slide:
"keep top 13% and bottom 18% free of text; keep right 11% free".

## Rascunho de layout em HTML (opcional)

O `assets/template-carrossel.html` usa layout pequeno escalado na exportação
(`scripts/exportar_slides.py`): `4:5` = 420×525, `1:1` = 420×420,
`9:16` = 405×720 → saída com 1080 px de largura. Serve só como **referência de
composição** para o Codex, nunca como peça final.

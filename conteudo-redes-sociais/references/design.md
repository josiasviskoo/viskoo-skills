# Sistema visual

## Paleta a partir de uma cor

Do **único** hex principal da marca, derive 6 tokens. Vão para `marca.cores` no `plano.json`, cada um com o seu papel (e para as variáveis CSS do rascunho HTML opcional):

| Token CSS | Regra | Uso |
|---|---|---|
| `--marca` | cor informada | barra de progresso, ícones, tags em fundo claro |
| `--marca-clara` | principal ~20% mais clara | tags em fundo escuro, pílulas |
| `--marca-escura` | principal ~30% mais escura | texto do botão CTA, início do gradiente |
| `--fundo-claro` | off-white tingido (nunca `#fff` puro): quente → creme, fria → cinza-azulado | slides claros |
| `--borda-clara` | um tom mais escuro que o fundo claro | divisórias |
| `--fundo-escuro` | quase preto com leve tom da marca (quente `#1A1918`, fria `#0F172A`) | slides escuros |

Gradiente da marca:
`linear-gradient(165deg, var(--marca-escura) 0%, var(--marca) 50%, var(--marca-clara) 100%)`

Cálculo rápido em Python (HSL):

```python
import colorsys
def ajustar(hex_, fator):            # fator > 0 clareia, < 0 escurece
    r, g, b = (int(hex_[i:i+2], 16)/255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l + fator * (1 - l if fator > 0 else l)))
    return '#%02X%02X%02X' % tuple(round(c*255) for c in colorsys.hls_to_rgb(h, l, s))
# ajustar('#E85D3A', 0.20) → clara ; ajustar('#E85D3A', -0.30) → escura
```

Se o usuário passar um site ou materiais da marca, extraia as cores de lá.

## Tipografia (Google Fonts)

| Estilo | Título | Corpo |
|---|---|---|
| Editorial / premium | Playfair Display | DM Sans |
| Moderno / limpo | Plus Jakarta Sans 700 | Plus Jakarta Sans 400 |
| Acolhedor | Lora | Nunito Sans |
| Técnico / afiado | Space Grotesk | Space Grotesk |
| Ousado / expressivo | Fraunces | Outfit |
| Clássico / confiável | Libre Baskerville | Work Sans |
| Arredondado / amigável | Bricolage Grotesque | Bricolage Grotesque |
| Impacto (posts virais) | Montserrat 900 / Poppins 800 | Inter |

Máximo de 2 famílias e 3 papéis (título / corpo / CTA). Fontes com bons
acentos para PT-BR (todas acima têm).

## Escala tipográfica

No `plano.json`, descreva a hierarquia em palavras ("headline very large,
about 3x the body size; small uppercase tag with wide letter-spacing"). O
Codex trabalha melhor com proporções relativas do que com valores em px. A
tabela abaixo serve de guia e vale para o rascunho HTML.

O template trabalha em layout de **420 px** (escala ×2,57 na saída de 1080 px):

| Elemento | No template (420 px) | Equivalente em 1080 px | Peso |
|---|---|---|---|
| Número gigante | 44–48 px | 112–120 px | 900 |
| Título | 28–34 px | 72–88 px | 600–800 |
| Corpo | 14–15 px | 36–39 px | 400 |
| Tag / rótulo | 10 px, caixa alta, `letter-spacing: 2px` | 26 px | 600 |
| Número de passo | 26 px, peso 300 | 67 px | 300 |
| Texto pequeno | 11–12 px | 28–31 px | 400–500 |

Títulos: `letter-spacing: -0.3 a -0.5px`, `line-height: 1.1–1.15`.
Corpo: `line-height: 1.5–1.55`.

Se gerar HTML direto em 1080 px (sem o template), use: número 96–120 px,
título 48–64 px, corpo 24–28 px, legenda 18–22 px.

## Contraste e legibilidade

- Mínimo **4,5:1** (WCAG AA) entre texto e fundo; 3:1 para títulos grandes.
- Texto sobre foto: overlay `rgba(255,255,255,.35)` (fundo claro) ou
  `rgba(0,0,0,.45)` (fundo escuro), faixa sólida ou desfoque. Sempre declare qual.
- Coloque o texto na área mais "quieta" da imagem, nunca sobre o ponto focal.
- Teste de miniatura: reduza a ~150 px de largura. O título ainda se lê?

## Layout

- **Um ponto focal** por peça (foto do produto, ilustração ou tipografia).
- Liderado por foto → título no terço superior ou inferior sobre faixa escura/desfocada.
- Liderado por tipografia → o título **é** o ponto focal; pouca imagem.
- Carrossel → grade idêntica em todos os cards; só o conteúdo muda.
- Regra dos terços e bastante espaço negativo.

## Consistência entre slides

| Elemento | Manter igual em todos |
|---|---|
| Fundo | mesma paleta (variações claro/escuro/marca são intencionais) |
| Fonte | mesmas famílias |
| Alinhamento | sempre à esquerda ou sempre centralizado |
| Margens | mesmo padding |
| Cor de destaque | a mesma |
| Numeração | mesmo formato |

## Princípios

1. Todo slide é exportável: seta e barra fazem parte da imagem.
2. Alternância claro/escuro cria ritmo.
3. Par de fontes: display para impacto, corpo para leitura.
4. Paleta derivada de uma cor deixa tudo coeso.
5. O último slide é especial: sem seta, barra cheia, CTA claro.
6. Iterar rápido: prévia, ajuste pontual, nada de refazer do zero.

---
name: conteudo-redes-sociais
description: >
  Cria conteúdo visual para redes sociais em português: carrosséis (Instagram,
  LinkedIn, X, Facebook), posts estáticos, stories, capas de Reels/TikTok,
  thumbnails de YouTube, pins de Pinterest, legendas e hashtags. O Claude faz
  briefing, copy com gancho, sistema visual e os prompts; TODAS as imagens
  finais são geradas pelo Codex CLI (ChatGPT / gpt-image) via script, ajustadas
  ao tamanho exato (1080×1350, 1080×1080, 1080×1920…), revisadas e entregues com
  prévia deslizável, PDF para LinkedIn, legenda e hashtags. Use sempre que o
  usuário pedir carrossel, "fazer carrossel", slides para Instagram/LinkedIn,
  post, arte, card, story, capa, thumbnail, banner, legenda, hashtags, "algo
  para postar sobre X" ou adaptar um design para várias redes, mesmo sem citar
  a plataforma.
---

# Conteúdo para Redes Sociais (imagens pelo Codex)

Transforma uma mensagem em peças prontas para postar. O princípio que governa
tudo: **uma peça social é lida em menos de 2 segundos**. Uma mensagem, um ponto
focal, um CTA.

**Divisão de trabalho (regra fixa):**

| Quem | Faz |
|---|---|
| **Claude** | briefing, estratégia, copy, sistema visual, `plano.json` (prompts), revisão visual das imagens, legenda e hashtags |
| **Codex (ChatGPT)** | **gera e edita todas as imagens finais** com a ferramenta `image_gen` |
| **Scripts** | chamam o Codex, ajustam o tamanho exato, montam prévia, folha de revisão e PDF |

Nunca entregue como final uma imagem feita pelo Claude (HTML, SVG ou PIL
desenhando a peça). O HTML só aparece como **rascunho de layout opcional**,
usado como referência para o Codex (veja o Passo 5).

## Na plataforma Viskoo (modo agente)

Quando a skill roda pela plataforma (existe `entrada/contexto.md` na pasta de trabalho), valem estes ajustes:

- **Onde está a skill:** `<skill>` = `.claude/skills/conteudo-redes-sociais` (relativo à pasta de trabalho).
- **Briefing já respondido:** `entrada/contexto.md` traz o cliente (informações e **regras do cliente**), o post ou a
  tarefa e as respostas da pessoa (`formato`, `redes`, `tema`, `enxuto`). Marca, cores e logo vêm de `marca/`; fotos e
  referências, de `entrada/materiais/`. Pule as perguntas do Passo 1 e infira o resto.
- **Sem aprovação no meio:** não há como esperar o "aprovado" dos Passos 3 e 7. Escreva o roteiro, gere, faça a
  **sua** revisão (Passo 7, item 1) com os ajustes pontuais e entregue. Ajustes pedidos pela pessoa viram nova execução.
- **Pasta do projeto:** `posts/<tema>/` dentro da pasta de trabalho. Ao final, copie para `saida/`: os PNGs de
  `slides/` (ou `variante-A/` e `variante-B/`), `carrossel.pdf` quando houver, `folha.png`, `previa.html` e um
  `legenda.md` com legenda, hashtags e texto alternativo de cada peça. A legenda também vai como resposta de texto.
- **Codex indisponível** (`codex login status` falhou): gere os prompts com `--prompts`, copie `prompts/` para
  `saida/` e explique em `saida/LEIA-ME.md` como colar no ChatGPT. Nunca substitua por imagem feita pelo Claude.
- **Progresso:** uma linha em `PROGRESSO.txt` a cada passo (roteiro, plano, geração slide a slide, revisão, entrega).
- **Precedência:** o que a pessoa respondeu > regras do cliente > esta skill. Nunca usar travessão (—).

## Arquivos desta skill

| Arquivo | Quando usar |
|---|---|
| `scripts/gerar_com_codex.py` | gera/regenera/ajusta as imagens via Codex a partir do `plano.json` |
| `scripts/montar_previa.py` | prévia deslizável, `folha.png` para revisão e PDF |
| `assets/exemplo-plano.json` | plano de carrossel (7 slides) para copiar |
| `assets/exemplo-plano-anuncio.json` | plano de lote de anúncios (Meta ADS), formatos 1:1 e 9:16 |
| `assets/exemplo-plano-ab.json` | plano de post orgânico com variantes A/B |
| `references/codex.md` | **schema do plano**, como escrever prompts para o Codex, ajustes, solução de problemas |
| `references/plataformas.md` | dimensões, proporções, zonas seguras, formatos aceitos pelo script |
| `references/carrossel.md` | estruturas de carrossel, ganchos, psicologia do swipe |
| `references/design.md` | paleta a partir de uma cor, fontes, hierarquia, contraste |
| `references/copy-legendas.md` | ganchos, legenda, CTA, hashtags, adaptação multi-rede |
| `assets/template-carrossel.html` + `scripts/exportar_slides.py` | rascunho de layout opcional (referência para o Codex) |
| `scripts/embutir_imagem.py` | embute foto em base64 no rascunho HTML |

## Pré-requisitos (verifique uma vez por sessão)

```bash
codex login status          # deve dizer "Logged in using ChatGPT"
python3 -c "import PIL"     # senão: pip install pillow
```

Sem Codex: `npm i -g @openai/codex && codex login`. Não precisa de
`OPENAI_API_KEY`, porque o Codex usa a assinatura do ChatGPT. Se o Codex não
estiver disponível, **pare e avise o usuário**. Não substitua por imagens
feitas pelo Claude.

## Modos de trabalho (escolha no briefing)

| Modo | Quando | No `plano.json` |
|---|---|---|
| **Carrossel** | conteúdo educativo, lista, tutorial, história | `"modo": "carrossel"` (padrão com >1 peça): barra, contador, seta; slide 1 é a referência de estilo |
| **Post / peça única** | post de feed, story, thumbnail, pin | `"modo": "post"`, 1 item em `slides` |
| **Anúncio (Meta ADS)** | criativos de tráfego pago | `"modo": "anuncio"`: cada peça com **ângulo, benefício, imagem, headline e design diferentes**; logo no canto (sem distorção); **tag de cidade só se o anúncio for local**; grafismo de apoio; botão de CTA; uma fonte da marca. Lote típico: 3 em `1:1` + 3 em `9:16` |
| **Variantes A/B** | o cliente escolhe entre 2 designs | `"variantes": {"A": {…}, "B": {…}}`: mesmo texto, design **totalmente** diferente (layout, cena, enquadramento, cor dominante, tipografia), cada variante com sua referência |

**Orgânico enxuto** (opcional, combina com post, carrossel e A/B): arte só
com **headline + subheadline**, sem logo (o logo entra apenas como referência
de paleta), sem tag de cidade, botão ou lista; CTA, cidade e detalhes vão para
a legenda. Carrossel nesse estilo: no máximo 4 slides e `"ui": false`.

## Passo 1: briefing (rápido, sem travar)

Pergunte **de uma vez só** apenas o que falta:

1. **Mensagem**: o que o post diz, em uma frase? Qual a ação (CTA)?
2. **Rede e formato**: carrossel, post único, story, capa, thumbnail? Uma ou várias redes?
3. **Marca**: nome, @, cor principal (hex ou descrição), logo, fontes.
4. **Tom e estilo visual**: profissional, divertido, minimalista; ilustração, foto realista, tipográfico, 3D.
5. **Imagens próprias**: logo, foto do rosto, produto, prints (caminhos de arquivo). Viram referências para o Codex.

**Infira em vez de perguntar**: tom pela rede (LinkedIn → profissional, TikTok
→ energético), cores de materiais da marca, idioma **português (BR)**. Com
mensagem e rede claras, declare as suposições e siga.

## Passo 2: formato

| Peça | Final | `formato` no plano |
|---|---|---|
| Carrossel Instagram / LinkedIn (recomendado) | 1080×1350 | `4:5` |
| Post quadrado / carrossel X e Facebook | 1080×1080 | `1:1` |
| Story, Reels, TikTok, Shorts | 1080×1920 | `9:16` |
| Imagem de post X | 1200×675 | `16:9` |
| Thumbnail YouTube | 1280×720 | `yt` |
| Post de link LinkedIn | 1200×627 | `1.91:1` |
| Pin Pinterest | 1000×1500 | `2:3` |

Use 4:5 no feed. Para várias redes: uma **peça-mestre** + adaptações (cada uma
com seu `formato` no plano). Nunca estique a mesma imagem.

## Passo 3: roteiro (copy antes do visual)

- **Título**: ≤ 10 palavras, específico. **Corpo**: ≤ 30–40 palavras por slide (post único: ≤ 2 linhas).
- **CTA**: 2–4 palavras com verbo. **Uma ideia por slide.**
- Slide 1 / capa: gancho forte (fórmulas em `references/carrossel.md`); nunca o nome da marca como título.
- Anúncio: headline persuasiva por peça, cada uma com um ângulo (dor, rapidez, preço, prova, autoridade, desejo…).
- **Sem travessão** (— ou –) nos textos da arte: use ponto, vírgula ou dois-pontos. O script avisa se encontrar.
- Nunca invente números, preços, porcentagens ou depoimentos: só o que o briefing trouxer.

Mostre o roteiro como tabela (nº, tipo, fundo, título, corpo) e ajuste com o
usuário **antes** de gerar. Mudar texto é grátis; regenerar imagem custa tempo
e cota.

**Menos texto = imagem melhor.** O gerador acerta textos curtos com alta
fidelidade; parágrafos longos aumentam a chance de erro.

## Passo 4: sistema visual

Defina e registre no plano:

1. **Paleta**: 5 hex derivados da cor principal (`references/design.md`), com papéis claros.
2. **Tipografia**: descreva o estilo ("serifada editorial de alto contraste,
   tipo Playfair Display"). O Codex aproxima; não garante a fonte exata.
3. **`estilo`**: uma frase em inglês que vale para todas as peças (meio,
   acabamento, margens, alinhamento). É o que mantém o carrossel coeso.
4. **Ritmo**: alterne fundo claro / escuro / gradiente da marca; CTA no gradiente.
5. **`evitar`**: lista negativa (ex.: "stock-photo look", "3D emoji").

## Passo 5: escrever o `plano.json`

1. Crie a pasta do projeto (ex.: `./posts/<tema>/`) e copie `assets/exemplo-plano.json` como `plano.json`.
2. Preencha marca, `estilo`, `formato` e um item em `slides` por peça, com
   `objetivo`, `fundo`, `visual`, `layout` e `textos` (verbatim, em PT-BR).
3. Referências (logo, foto do produto, rosto, artes de referência) vão em
   `referencias` (global, da variante ou do slide), com o **papel** de cada
   imagem descrito. Exemplos de papel: "brand logo: reproduce EXACTLY, no
   distortion, small top-left" (anúncio) · "brand logo ONLY to read the color
   palette, must NOT appear" (orgânico) · "design reference: follow its layout
   and typography; never copy its text, logos or people".
4. Schema completo, boas práticas de prompt e exemplos: **`references/codex.md`**.

**Rascunho de layout (opcional)**: quando a composição precisa ser muito
precisa, monte o slide no `assets/template-carrossel.html`, exporte com
`scripts/exportar_slides.py` e passe o PNG como referência
(`"papel": "layout reference: follow composition and text placement, render as a polished final design"`).

Antes de gastar, confira os prompts montados:

```bash
python3 <skill>/scripts/gerar_com_codex.py posts/<tema>/plano.json --prompts
```

## Passo 6: gerar com o Codex

```bash
python3 <skill>/scripts/gerar_com_codex.py posts/<tema>/plano.json -j 2
python3 <skill>/scripts/montar_previa.py posts/<tema> --pdf
```

Com variantes, cada uma fica em `variante-A/`, `variante-B/`, e a prévia gera
`folha-variantes.png` para comparar. `--variante B` (re)gera só uma delas.

- O slide 1 é gerado primeiro e vira **referência de estilo** dos demais (consistência).
- Leva ~1 min por imagem; com `-j 2` ou `-j 3` roda em paralelo. Use
  `timeout` ≥ 600000 ms no Bash ou rode em segundo plano.
- Saídas: `slides/` (finais no tamanho exato), `bruto/` (originais e versões
  anteriores), `prompts/`, `logs/`, `previa.html`, `folha.png`, `carrossel.pdf`.

## Passo 7: revisão (obrigatória)

1. **Claude revisa primeiro**: leia `folha.png` e, para conferir o texto,
   cada `slides/slide_XX.png`. Cheque palavra por palavra: acentos, "ç",
   palavras trocadas ou duplicadas, texto cortado nas bordas, contraste, a
   barra "n/total" correta, a seta ausente no último slide e o estilo consistente.
2. Corrija o que achar com **ajuste pontual** (a imagem atual vai como alvo de edição):
   ```bash
   python3 <skill>/scripts/gerar_com_codex.py plano.json --ajustar 4 \
     --instrucao 'fix the headline text to exactly "Mais salvamentos"'
   ```
   Para algo totalmente errado: `--slides 4` (gera do zero com o estilo do slide 1).
   **Atualize o `plano.json`** sempre que o texto mudar, para manter o plano como fonte da verdade.
3. Mostre ao usuário a `previa.html` (abra com `xdg-open`/`open`) e a folha, e pergunte:
   **"Quais slides precisam de ajuste antes de finalizar?"**
4. Ajuste **só** os slides citados. Finalize apenas com aprovação explícita
   ("aprovado", "pode finalizar", "ok"). Depois de cada rodada, rode
   `montar_previa.py` de novo.

## Passo 8: entregar

- Caminhos dos PNGs finais em `slides/` (e `carrossel.pdf` para o LinkedIn).
- **Legenda** pronta (gancho na 1ª linha, valor, CTA) e hashtags (`references/copy-legendas.md`); salve também em `plano.json > legenda`.
- **Texto alternativo** por slide.
- Os prompts finais estão em `prompts/` para reuso.

## Checklist de qualidade

- [ ] Todas as imagens finais vieram do Codex (nenhuma desenhada pelo Claude).
- [ ] Dimensões exatas (o script garante); formato certo por rede.
- [ ] Texto conferido palavra por palavra pelo Claude; acentuação PT-BR correta.
- [ ] Slide 1 com gancho + indicação de swipe; uma ideia por slide; ≤ 40 palavras.
- [ ] Estilo, paleta, margens e tipografia consistentes em todos os slides.
- [ ] Nada importante cortado nas bordas; contraste ≥ 4,5:1.
- [ ] Último slide: CTA claro, sem seta, barra "N/N".
- [ ] Sem estatísticas inventadas; `plano.json` em sincronia com o texto final.
- [ ] Sem travessão; sem ícone solto no canto sem informação; sem excesso de ícones e imagens.
- [ ] Anúncio: logo sem distorção, CTA presente, tag de cidade só se local, peças realmente diferentes entre si.
- [ ] Variantes A/B: mesmo texto e designs claramente distintos (se parecidas, regenere a B mais longe da A).
- [ ] Legenda, hashtags e texto alternativo entregues.

## Erros comuns

| Erro | Correção |
|---|---|
| Texto com erro ou letra trocada | `--ajustar N --instrucao 'fix … to exactly "…"'`; encurte o texto se insistir |
| Slides com estilos diferentes | Gere o slide 1 primeiro (padrão); reforce `estilo`; regenere com `--slides` |
| Texto colado na borda / cortado | A margem de segurança já está no prompt; regenere pedindo "more padding" |
| Marca/logo distorcido | Passe o logo como referência com papel "exact logo, do not redraw" ou peça o espaço vazio |
| Codex não salvou a imagem | O script recupera de `~/.codex/generated_images`; veja `logs/slide_XX.jsonl` |
| Tempo esgotado | `--timeout 900`, menos paralelismo (`-j 1`) |
| Plano desatualizado após ajustes | Atualize `textos` no `plano.json` a cada mudança |
| Variante B parecida com a A | Reescreva a `descricao` da B (outro layout, cena e cor dominante) e rode `--variante B` |
| Logo distorcido no anúncio | `--ajustar N --instrucao 'restore the logo exactly as Image 2, original proportions'` com o logo nas referências |

## Sem Codex CLI?

Cada `prompts/slide_XX.txt` é autossuficiente: dá para colar no ChatGPT anexando
as imagens listadas em "Input images", na mesma ordem. Gere com
`--prompts` e entregue os arquivos ao usuário.

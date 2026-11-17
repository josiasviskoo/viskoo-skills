# Gerando as imagens com o Codex

## Como funciona

`scripts/gerar_com_codex.py` lê o `plano.json` e, para cada peça:

1. monta um prompt estruturado no formato que a skill `imagegen` do Codex
   espera (`Use case / Asset type / Primary request / … / Text (verbatim) /
   Constraints / Avoid`);
2. roda `codex exec --skip-git-repo-check --ephemeral -s workspace-write -C bruto/ [-i referências] --json`,
   com o prompt via stdin, pedindo **uma** chamada da ferramenta interna `image_gen`;
3. pega a imagem salva em `bruto/` (ou, como plano B, a mais nova em
   `~/.codex/generated_images/`);
4. redimensiona e recorta pelo centro para o tamanho final exato em `slides/`.

A ferramenta interna usa o login do ChatGPT (sem `OPENAI_API_KEY`) e consome
a cota de imagens da assinatura. Cada imagem leva ~50–80 s.

## Schema do `plano.json`

```jsonc
{
  "projeto": "slug-do-projeto",
  "pasta": ".",                       // opcional: onde salvar (relativo ao plano)
  "modo": "carrossel",                // carrossel | post | anuncio (padrão: carrossel se >1 peça)
  "tipo": "Instagram carousel slide", // vai para "Asset type" (ex.: "Meta Ads static creative", "YouTube thumbnail")
  "formato": "4:5",                   // 4:5 | 1:1 | 9:16 | 16:9 | yt | 1.91:1 | 2:3
  "caso_de_uso": "ads-marketing",     // slug da taxonomia do imagegen (veja abaixo)
  "ui": true,                         // barra de progresso + contador + seta (padrão: true se >1 slide)
  "marca": {
    "nome": "Sua Marca",              // aparece no 1º e no último slide (controle: "mostrar_marca" no slide)
    "handle": "@suamarca",            // usado na prévia; inclua em "textos" se quiser na arte
    "cores": { "primary accent": "#E85D3A", "light background": "#FAF6F1" },
    "fontes": { "headlines": "high-contrast serif like Playfair Display" }
  },
  "estilo": "frase em inglês aplicada a TODAS as peças",
  "layout_geral": "sistema de layout comum (opcional)",
  "variantes": {                      // opcional: mesmo conteúdo, designs diferentes
    "A": { "descricao": "layout, cena, cor dominante da A",
           "referencias": [ { "arquivo": "ref-a.jpg", "papel": "design reference for variant A" } ],
           "estilo": "…", "evitar": ["…"],          // sobrescrevem/somam ao global
           "slides": [ { "layout": "…" } ] },       // sobrescritas por slide, na mesma ordem
    "B": { "descricao": "…", "referencias": [ … ] }
  },
  "restricoes": ["…"],                // extras para todas as peças
  "evitar": ["…"],                    // lista negativa para todas as peças
  "referencias": [                    // imagens enviadas em TODAS as gerações
    { "arquivo": "logo.png", "papel": "brand logo: reproduce exactly, small, top-left" }
  ],
  "legenda": "legenda final do post",
  "slides": [
    {
      "tipo": "capa",
      "objetivo": "hook cover slide that stops the scroll",   // Primary request
      "fundo": "warm off-white #FAF6F1",                       // Scene/backdrop
      "visual": "o que desenhar (ilustração, foto, ícone)",    // Subject
      "layout": "onde fica cada coisa",                        // Composition
      "textos": {                                              // TEXTO EXATO em PT-BR
        "tag": "GUIA RÁPIDO", "titulo": "…", "subtitulo": "…",
        "corpo": "…", "itens": ["…", "…"], "cta": "…", "rodape": "…"
      },
      "referencias": [ { "arquivo": "produto.jpg", "papel": "product photo: keep the product identical" } ],
      "formato": "9:16",              // opcional: sobrescreve o global (peças multi-rede)
      "caso_de_uso": "product-mockup",// opcional
      "ui": false,                    // opcional
      "mostrar_marca": false,         // opcional
      "restricoes": [], "evitar": [],
      "prompt": "…"                   // opcional: prompt livre que substitui toda a montagem
    }
  ]
}
```

Caminhos de `arquivo` são relativos à pasta do plano.

### Slugs úteis de `caso_de_uso`

`ads-marketing` (padrão, posts e carrosséis) · `infographic-diagram`
(dados/fluxos) · `product-mockup` (produto) · `photorealistic-natural`
(lifestyle/foto) · `illustration-story` · `stylized-concept` (3D/estilizado) ·
`productivity-visual` (slides de negócio). Edições: `precise-object-edit`,
`text-localization`, `background-extraction`, `style-transfer`, `compositing`.

## Regras que o script sempre injeta

Margem de segurança de 6%; contraste AA; sem marca d'água ou logos extras;
**sem travessão**; ícones só junto da informação (nunca soltos no canto);
**não inventar números, preços ou promessas**; e, havendo referências, usar
delas só a linguagem visual. Somam-se a isso as `restricoes` e `evitar` do
plano, da variante e do slide. O script também **avisa** quando algum texto tem
travessão ou mais de 40 palavras, e **falha** se uma referência não existir.

## Escrevendo bons campos

- **Inglês nas descrições, PT-BR nos textos.** `estilo`, `visual`, `layout`,
  `fundo` e `objetivo` em inglês; `textos` sempre em português, exatamente como
  devem aparecer.
- **Textos curtos.** Título ≤ 10 palavras, corpo ≤ 25 palavras, itens ≤ 6 palavras cada.
- **Hierarquia explícita no `layout`**: "headline large at lower-middle,
  body below, tag above headline".
- **Paleta com hex e papéis.** O script injeta `marca.cores` em todos os prompts.
- **`estilo` único** para o carrossel inteiro. Não varie entre slides.
- **Nada de texto em `visual`/`layout`** que não esteja em `textos`: o prompt
  diz "no other words", e texto citado fora da lista gera conflito.
  Exceção: rótulos já listados em `textos`.
- **Números grandes** ("01") podem ser descritos em `visual`, pois são elementos gráficos.
- **Fotos reais de pessoas/produtos** → passe como referência e descreva o
  papel ("keep the person's face identical"). Não peça para inventar o rosto
  de alguém real.
- **Peça única (story, thumbnail, pin)**: plano com 1 item em `slides`; não há
  barra nem seta.

## Comandos

```bash
S=<pasta-da-skill>/scripts
python3 $S/gerar_com_codex.py plano.json --prompts         # só monta e mostra (grátis)
python3 $S/gerar_com_codex.py plano.json -j 2              # gera tudo
python3 $S/gerar_com_codex.py plano.json --slides 3,5      # regenera do zero esses slides
python3 $S/gerar_com_codex.py plano.json --ajustar 3 --instrucao 'change only …'
python3 $S/gerar_com_codex.py plano.json --sem-referencia-de-estilo   # peças independentes
python3 $S/gerar_com_codex.py plano.json --modelo <modelo> --timeout 900 --tentativas 2
python3 $S/montar_previa.py <pasta> --pdf
```

### Regenerar vs. ajustar

| Situação | Use |
|---|---|
| Uma palavra errada, cor de um elemento, botão, mover algo | `--ajustar N --instrucao '…'` (preserva o resto) |
| Composição ruim, estilo destoando, ideia errada | corrija o plano e rode `--slides N` |
| Mudou o estilo global | regenere o slide 1 e depois os outros (`--slides 1` e depois `--slides 2,3,…`) |

Instruções de ajuste em inglês, específicas e com texto exato entre aspas:
`'change only the headline to exactly "Seu gancho é vago demais"; keep everything else identical'`.

Cada nova geração versiona a anterior (`bruto/slide_03_v1.png`, `_v2`…). Para
voltar, copie a versão desejada para `bruto/slide_03.png` e rode
`--ajustar 3 --instrucao 'no changes'`, ou só redimensione manualmente.

## Revisão pelo Claude

Depois de cada geração:

1. `montar_previa.py` → leia `folha.png` (visão geral: consistência, ritmo, contraste).
2. Leia cada `slides/slide_XX.png` em tamanho real e compare **letra por letra**
   com `textos`: acentos (ã, é, ç), plural/singular, palavras duplicadas,
   pontuação, número do contador.
3. Liste os problemas encontrados, corrija com `--ajustar`, rode a prévia de
   novo e só então mostre ao usuário.

## Solução de problemas

| Sintoma | Causa / solução |
|---|---|
| `Codex CLI não encontrado` | `npm i -g @openai/codex` e `codex login` |
| `codex login status` não mostra ChatGPT | `codex login` (escolha a conta ChatGPT) |
| "o Codex não gerou imagem" | Veja `logs/slide_XX.jsonl`. Cota de imagens esgotada, recusa de conteúdo ou recurso desativado (`codex features list | grep image_generation` deve ser `true`) |
| Tempo esgotado | `--timeout 900`, `-j 1` |
| Imagem com proporção diferente | O script recorta pelo centro; se cortou texto, regenere pedindo mais margem |
| Texto insiste em sair errado | Encurte a frase, use palavras mais comuns, ou divida em dois slides |
| O Codex respondeu com código/SVG | Rode de novo; a instrução já proíbe isso. Se persistir, atualize o Codex (`codex update`) |

Fallback por API (`OPENAI_API_KEY` + `gpt-image-2`) existe dentro da skill
`imagegen` do próprio Codex. Use só se o usuário pedir explicitamente.

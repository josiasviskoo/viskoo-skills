# Carrosséis: estrutura, ganchos e componentes

## Slide 1: o gancho

O slide mais importante. Precisa parar a rolagem em menos de 1 segundo.

| Tipo de gancho | Exemplo |
|---|---|
| Afirmação polêmica | "Você está usando IA errado" |
| Número + benefício | "7 ferramentas que substituem seu designer" |
| Pergunta que dói | "Por que seus carrosséis têm 0 salvamentos?" |
| Resultado concreto | "Como saímos de 0 a R$ 1 mi em 12 meses" (só com dado real) |
| Inversão de expectativa | "Mais esforço no design = menos alcance" |
| Contrário ao senso comum | "Pare de escrever posts no blog (faça isso)" |
| Antes/depois | Mostrar a transformação lado a lado |

Regras:
- Nunca comece com o nome da marca como título.
- Prova visual no slide 1 quando possível (print, resultado, número real).
- O gancho promete algo que os próximos slides **entregam**.
- Inclua uma indicação de swipe ("Arraste →" e/ou a seta lateral).

## Sequências

### Padrão (7 slides)

| # | Tipo | Fundo | Propósito |
|---|---|---|---|
| 1 | Capa | claro | Gancho + logo |
| 2 | Problema | escuro | A dor: o que está quebrado ou ultrapassado |
| 3 | Solução | marca (gradiente) | A resposta; caixa de citação opcional |
| 4 | Benefícios | claro | O que a pessoa ganha (lista com ícones) |
| 5 | Detalhes | escuro | Profundidade: diferenciais, especificações |
| 6 | Como fazer | claro | Passos numerados |
| 7 | CTA | marca (gradiente) | Logo, frase, botão. **Sem seta. Barra 100%.** |

### Educativo / dicas (lista)

| # | Tipo | Fundo |
|---|---|---|
| 1 | Capa: "5 truques de CSS que você precisa saber" | claro |
| 2 a N | Uma dica por slide, numerada (01, 02…) | alternando |
| Último | CTA: "Siga para mais dicas" | marca |

Use para "X ferramentas", "X erros", "X dicas". Deixe **a melhor dica por
último**: recompensa quem chegou ao fim.

### Tutorial (7 slides)

Capa → Contexto/por quê (escuro) → Passo 1, 2, 3 (alternando) → Resultado
esperado (escuro) → CTA (marca).

### História / estudo de caso

Capa ("Como crescemos de 0 a…") → Começo → Desafio → O que tentamos e falhou →
O que funcionou → Resultado com números → Lição + CTA.

### Antes / depois

Capa ("Redesenhei esta landing page") → Antes → Problema apontado → Depois →
Melhoria explicada → Resultado → CTA ("Quer uma análise? Me chama no direct").

### Comparação (5 slides)

Capa (o que será comparado, claro) → Opção A (claro) → Opção B (escuro) →
Veredito (marca) → CTA (escuro).

### Ferramentas / curadoria

Capa → 2 ferramentas por slide com logo + uma linha → "Salve para depois 🔖".

**Regras gerais**: adapte ao tema (nem todo carrossel precisa de 7 slides),
alterne claro/escuro, termine no CTA.

## Psicologia do swipe

| Princípio | Aplicação |
|---|---|
| Lacuna de curiosidade | O gancho promete valor que exige deslizar |
| Progresso numerado | "3/7" e barra de progresso criam vontade de completar |
| Continuidade visual | Design consistente sinaliza "tem mais" |
| Valor crescente | O melhor ponto no fim recompensa quem completou |
| Pista de swipe | Seta lateral em todos os slides, menos o último |
| Salvamento | Conteúdo de referência (listas, passos, checklists) gera "salvar" |

## Elementos obrigatórios em todo slide

1. **Barra de progresso** (rodapé): trilho de 3 px, preenchimento
   `(índice+1)/total`, contador "1/7" ao lado. Claro: trilho `rgba(0,0,0,.08)`,
   preenchimento na cor da marca. Escuro: trilho `rgba(255,255,255,.12)`,
   preenchimento branco.
2. **Seta de swipe** (borda direita, 48 px): chevron sutil sobre um degradê.
   Some no último slide.
3. **Padding que livra a UI**: conteúdo com `padding-bottom` ≥ 52 px (no layout
   de 420 px) para nunca encostar na barra.

Com `"ui": true` (padrão em carrosséis), o `gerar_com_codex.py` pede os
elementos 1 e 2 ao Codex com o percentual e o contador certos para cada slide.
O Claude confere na revisão.

## Layout

- Padding lateral: 36 px (no layout de 420 px).
- Capa/CTA: conteúdo centralizado verticalmente (`.centro`).
- Slides com bastante conteúdo: conteúdo alinhado embaixo (padrão do template).
- Numeração consistente: sempre `01, 02…` ou sempre `1., 2.`. Nunca misture.

## Componentes visuais

Descreva-os no campo `visual`/`layout` do slide no `plano.json` (em inglês),
por exemplo: "three list items with small orange sparkle bullets and thin
dividers", "translucent rounded quote box", "pill-shaped off-white button".

Equivalentes no rascunho HTML opcional (classes do template):

| Classe | Uso |
|---|---|
| `.tag` | Rótulo de categoria em caixa alta acima do título |
| `.titulo` / `.corpo` / `.pequeno` | Hierarquia de texto |
| `.numero-grande` | Número gigante de dica (01, 02…) |
| `.lista` > `.item` (`.ic` + `div > b + span`) | Lista de benefícios com ícone |
| `.passos` > `.passo` (`.n` + `div > b + span`) | Passos numerados |
| `.pilula` / `.pilula.riscada` | Pílulas de rótulo / "ferramenta antiga" riscada |
| `.citacao` | Caixa de prompt ou citação |
| `.botao` | Botão de CTA (só no último slide) |
| `.logo` | Logo: círculo com inicial ou SVG + nome da marca |
| `.amostras` > `span` | Amostras de cor |
| `img.bg` + `.overlay` | Foto de fundo com overlay para legibilidade |

## Texto por slide

| Regra | Valor |
|---|---|
| Máx. palavras por slide | 30–40 |
| Máx. linhas de corpo | 4–5 |
| Altura de linha do corpo | 1,5–1,6 |
| Ideias por slide | **1** |

---
name: reel-video
description: Estúdio de vídeo vertical 9:16 (Reels, Shorts, Stories, Meta Ads) para quem grava a si mesmo falando. Três modos. ROTEIRO, para criar roteiros de anúncio/reel com o template validado "Espelho Local" (engenharia reversa de um anúncio vencedor; briefing, roteiro cronometrado, teleprompter, shot list, hooks, checklist) para profissionais e negócios locais de serviço. EDIÇÃO, que corta a fala bruta (silêncios, "éé", gaguejos, retomadas) com o motor de corte e edita no motor "VSL com interface animada" (FULL/SPLIT, peças que entram na palavra, legenda que segue a boca, vídeos sobrepostos/B-roll ancorados na fala, −14 LUFS) e entrega render/reel-v1.mp4 verificado. COMPLETO, que vai do roteiro à gravação e à edição na mesma pasta de projeto. Use SEMPRE que pedirem "edita esse reel", "corta e edita", "monta esse bruto", "faz o reel/anúncio desse vídeo", "tenho a fala e os sobrepostos", "cria um roteiro/criativo/script de anúncio", "hook", "texto de gravação", "criativo igual ao vencedor", ou passarem vídeos falados para virar reel ou anúncio, mesmo sem citar a skill. NÃO serve para vídeo longo do YouTube, showreel sem alguém falando, carrossel ou copy de texto puro.
---

# reel · roteiro + corte + edição

Uma skill, três modos, uma pasta de projeto por vídeo. **Nunca publique nem envie o vídeo** (R9). **Nenhum nome de
terceiro** no vídeo nem nos arquivos (R11). As **regras da casa** (`regras-da-casa.md`) valem por cima de tudo.

## Na plataforma Viskoo (modo agente)

Quando a skill roda pela plataforma (existe `entrada/contexto.md` na pasta de trabalho), valem estes ajustes:

- **Onde está a skill:** `S=.claude/skills/reel-video` (relativo à pasta de trabalho). Use sempre `$S` no lugar de
  `~/.claude/skills/reel-video`.
- **O que você recebe:** `entrada/contexto.md` (cliente com informações e **regras do cliente**, post ou tarefa,
  respostas da pessoa: `etapa`, `objetivo`, `tema`, `roteiro`), `entrada/materiais/` (briefing, identidade e os
  vídeos/fotos dos links baixados) e `marca/` (logo e cores do cliente, para cards e peças do motor VSL).
- **Modo:** `etapa = Roteiro` → **ROTEIRO**; `etapa = Edição dos vídeos gravados` → **EDIÇÃO**. O modo COMPLETO não
  roda numa execução só (a pessoa precisa gravar no meio): entregue o roteiro e, depois da gravação, roda-se a edição.
  `objetivo` responde a dúvida orgânico × anúncio, não pergunte de novo.
- **Projeto:** crie a pasta do vídeo dentro da pasta de trabalho (`bash $S/novo-projeto.sh <slug> .`) e separe os
  arquivos de `entrada/materiais/` em `brutos/fala/`, `brutos/sobrepostos/` e `brutos/fotos/` pelo nome e pelo
  conteúdo (na dúvida, o vídeo em que alguém fala para a câmera é fala). Falta a fala na EDIÇÃO: pare e diga o que
  faltou em `saida/LEIA-ME.md`.
- **Sem conversa no meio:** não há como esperar aprovação. Decida pelo briefing e pelas regras do cliente, registre as
  suposições e entregue a versão 1; ajustes viram uma nova execução.
- **Entrega em `saida/`:** ROTEIRO → `roteiro.md`, `texto-de-gravacao.md`, `shot-list.md`, `checklist.md`. EDIÇÃO →
  `reel-v1.mp4` (o render verificado), a folha de quadros de `qa/` e `SOURCES.md`. Sempre um `saida/LEIA-ME.md`
  curto: o que foi feito, as suposições e o que a pessoa precisa conferir.
- **Progresso:** escreva uma linha em `PROGRESSO.txt` a cada etapa (briefing, roteiro, corte, transcrição,
  preparo, render, verificação), para a pessoa acompanhar.
- **Precedência:** o que a pessoa respondeu > regras do cliente > `regras-da-casa.md` > esta skill. Nunca usar
  travessão (—) em roteiro, legenda ou texto de tela; use hífen, vírgula ou dois pontos.

## Escolha o modo
| A pessoa… | Modo | Leia e siga |
|---|---|---|
| quer um roteiro, criativo, hook, texto de gravação ou briefing | **ROTEIRO** | `roteiro/ROTEIRO.md` |
| mandou vídeos gravados (fala, e talvez sobrepostos e fotos) para virar reel/anúncio | **EDIÇÃO** | `edicao/EDICAO.md` |
| quer o caminho todo: roteiro → ela grava → edição | **COMPLETO** | `roteiro/ROTEIRO.md`, depois `edicao/EDICAO.md` na mesma pasta, com `roteiro/framework/08-do-roteiro-a-edicao.md` |

Na dúvida entre reel **orgânico** e **anúncio** (muda a zona segura e o CTA), pergunte uma vez. Sem resposta: orgânico.

## O material que a pessoa grava
- **Fala**: ela falando para a câmera, num arquivo ou em várias partes → `brutos/fala/`.
- **Sobrepostos**: vídeos que cobrem a fala para ilustrar a cena (B-roll: mãos, equipamento, ambiente, tela) → `brutos/sobrepostos/`.
- **Fotos**: casos reais, antes/depois, prints, logos → `brutos/fotos/`.

A pasta de cada vídeo nasce com `bash $S/novo-projeto.sh <slug>` (`S=~/.claude/skills/reel-video`, ou `REEL_SKILL`):
`roteiro/ · brutos/{fala,sobrepostos,fotos}/ · corte/ · preparo/ · motor/ · assets/ · render/ · qa/ · entrega/`.
Os brutos nunca são apagados nem alterados; nada é escrito dentro da pasta da skill.

## Mapa da skill
```
SKILL.md                 este arquivo: escolhe o modo
regras-da-casa.md        R1–R11: rosto nunca coberto, SFX com parcimônia, material real, nenhuma palavra comida, −14 LUFS…
novo-projeto.sh          cria a pasta de um vídeo (roteiro, brutos, corte, motor, render…)
roteiro/                 MODO ROTEIRO · template "Espelho Local" (anúncio vencedor)
  ROTEIRO.md               o fluxo e as regras
  briefing/                questionário para o cliente preencher
  framework/               01 briefing · 02 estrutura 8 blocos · 03 template · 04 specs visuais · 05 saída
                           06 checklist · 07 exemplo aplicado · 08 do roteiro à edição
  scripts/                 checar-contaminacao.sh
  referencia-vencedor/     o anúncio original (SÓ ESTUDO: transcrição, decomposição, análise, frames)
edicao/                  MODO EDIÇÃO · corte + motor VSL
  EDICAO.md                o fluxo (corte → preparo → planta → render → entrega)
  ESTILO.md                a espec do motor VSL: layouts, movimento, legenda, peças, som, aceite, lições
  pele.json                os valores nativos (fontes, cinco cores, invariantes)
  corte/                   motor de corte: CORTE.md · references/EDICAO-BRUTA.md · scripts/ · exemplo/
  motor-vsl/               motor VSL: kit/ (intocado) · montar.mjs · sobrepostos.mjs · preparar.sh · ferramentas/ · exemplo/
  ferramentas/             juntar-falas.sh · preparar.py · rosto.py · ancoras.py · verificar.py · zona-segura.py
                           recortar.py · audio-final.sh · gerar-imagem.sh (Codex, quando falta material)
  anexos/                  quadros da referência e o antes × depois da cor
```

## Condução
- Diga em uma linha o modo e o que vai acontecer; avise antes de cada etapa lenta (transcrição, render).
- Dado de conteúdo que só a pessoa sabe (fato, preço, nome, técnica, autorização de foto) → pergunte; nunca invente.
- **Os motores não se reescrevem** (`edicao/motor-vsl/kit/`, `edicao/corte/scripts/`); **o template não vaza a
  referência** (`roteiro/referencia-vencedor/` é só leitura).
- Falhou a máquina (ffmpeg, whisper, node, Chrome)? `python3 $S/edicao/corte/scripts/0-checar.py` diagnostica.

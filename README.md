# Skills da plataforma Viskoo IA

Repositório **privado**. Cada pasta é uma skill: a plataforma lê este repositório e transforma cada skill num botão
no lugar certo (transcrição, cliente, tarefa, post ou chat). O cliente nunca vê este repositório.

```
ata-reuniao/            (cada skill: uma pasta na raiz, com o mesmo nome do id)
  viskoo.json      ← o manifesto: onde aparece, do que precisa, o que entrega
  SKILL.md         ← o processo (o que a IA segue)
  referencias/     ← opcional: outros .md que entram junto (modelos, exemplos)
```

## Catálogo

| Pasta | Botão | Modo | Aparece em |
|---|---|---|---|
| `ata-reuniao/` | 📝 Gerar ATA da reunião | texto | transcrição, cliente, chat |
| `extrator-tarefas/` | ✅ Extrair tarefas da reunião | texto | transcrição, chat |
| `roteiro-reels/` | 🎥 Roteiros de Reels (orgânico) | texto | post, cliente, tarefa, chat |
| `reel-video/` | 🎬 Reel em vídeo: roteiro e edição | agente | post, cliente, tarefa, chat |
| `conteudo-redes-sociais/` | 🖼️ Artes para redes sociais | agente | post, cliente, tarefa, chat |

`roteiro-reels` × `reel-video`: o primeiro é rápido e barato (texto), vários roteiros orgânicos de locução no método
gancho, desenvolvimento e fechamento. O segundo usa o template "Espelho Local" (8 blocos, teleprompter, shot list,
hooks), pensado sobretudo para anúncio de negócio local, e também **edita os vídeos gravados** até o MP4 final.

### O que o servidor precisa para as skills do modo agente

| Skill | Ferramentas | Rede |
|---|---|---|
| `reel-video` (edição) | `ffmpeg`, `whisper-cli` + modelo `ggml-large-v3-turbo.bin` (`WHISPER_MODEL`), Python 3 com `numpy` e `opencv-python-headless` (`mediapipe` opcional, via `VSL_PYTHON`), Node 20+, Google Chrome (`CHROME`) | `npm` na primeira preparação do motor (`hyperframes`, `gsap`, `playwright`); Codex só se faltar imagem |
| `reel-video` (roteiro) | nenhuma além do Claude | nenhuma |
| `conteudo-redes-sociais` | Codex CLI logado com ChatGPT (`codex login status`), Python 3 com `pillow` (`playwright` opcional) | acesso ao Codex/OpenAI para gerar as imagens |

Diagnóstico da edição: `python3 reel-video/edicao/corte/scripts/0-checar.py`. Cada uma também funciona fora da
plataforma, como skill comum do Claude Code (veja o `README.md` dentro da pasta).

## Versões

- `main` = **produção**: o que todo mundo usa. Cada commit vira a versão nova em até 30 minutos (ou na hora, em
  /regras › Skills › Catálogo › Atualizar agora).
- `teste` = **versão de teste**: só o administrador principal escolhe "Versão de teste" ao rodar uma skill.
  Teste no ramo `teste`, depois junte no `main`.
- Deu problema? Em /regras › Skills › Catálogo, **fixe a produção** num commit anterior (e solte quando corrigir).
- Cada execução registra o commit usado.

## O manifesto (`viskoo.json`)

```json
{
  "id": "ata-reuniao",                 // igual ao nome da pasta: minúsculas, números e hífen
  "nome": "Gerar ATA da reunião",       // o texto do botão
  "descricao": "...",                   // aparece no botão e no começo da tela
  "icone": "📝",
  "aparece_em": ["transcricao", "chat"],// transcricao | projeto | tarefa | post | chat
  "entradas": [ ... ],                  // do que a skill precisa (abaixo)
  "perguntas_ia": true,                 // a IA pode fazer até 3 perguntas curtas antes de rodar
  "materiais": true,                    // lê os links da pasta do projeto (briefing, identidade...)
  "modo": "texto",                      // texto (rápido, barato) | agente (pasta + scripts, caixa isolada)
  "nivel": "padrao",                    // rapido | padrao | pro (o modelo da IA)
  "saidas": [ ... ],                    // o que entrega (abaixo)
  "teto_usd": 1,                        // gasto máximo de uma execução (pela API)
  "minutos": 30                         // só no modo agente: tempo máximo
}
```

### Entradas

| tipo | o que é | de onde vem |
|---|---|---|
| `transcricao` | a transcrição inteira | do lugar onde clicou, ou a pessoa escolhe da lista |
| `projeto` | o cliente: informações, **regras do cliente**, materiais | do contexto, ou a pessoa escolhe |
| `tarefa` | a tarefa com notas e comentários | só do contexto (botão na tarefa) |
| `post` | o post do calendário editorial | só do contexto (botão no post) |
| `texto`, `texto_longo`, `data`, `numero` | campo para a pessoa preencher | pergunta |
| `escolha`, `multipla` | botões com `opcoes` | pergunta |
| `links` | links colados (Drive, sites, YouTube…) | pergunta (no modo agente, são baixados) |

Cada entrada: `{ "id", "tipo", "rotulo", "obrigatorio": true|false, "origem": "contexto" | "pergunta" | "contexto_ou_pergunta", "opcoes": [...], "ajuda": "..." }`.

### Saídas

| tipo | vai para |
|---|---|
| `documento` | `formato`: `docx` ou `md`; `destino`: `pasta` (pasta do cliente) — e sempre a Bandeja. `nome` com `{CLIENTE}`, `{data}`, `{titulo}` ou o id de uma entrada (`{tipo}`) |
| `texto` | a Bandeja (ou a pasta, com `destino: pasta`) |
| `tarefas` | sugeridas: a pessoa confere, edita, muda cliente e cria no gestor |
| `posts` | sugeridos: a pessoa confere e cria no calendário editorial |
| `arquivos` | só no modo agente: os arquivos que a skill salvou em `saida/` vão para a pasta do cliente e a Bandeja |

## Como a IA recebe a skill

- **Modo texto:** o `SKILL.md` e os outros `.md` da pasta, o contexto escolhido (transcrição, cliente com regras e
  materiais, tarefa, post), as respostas da pessoa e o formato de saída. A resposta já volta estruturada.
- **Modo agente:** uma pasta de trabalho com a skill em `.claude/skills/<id>/`, o contexto em `entrada/contexto.md`, os
  materiais baixados em `entrada/materiais/`, logo e cores em `marca/`. Os arquivos finais vão em `saida/`. Escreva a
  linha de progresso em `PROGRESSO.txt` (a pessoa vê). Sem internet para fora do que a skill precisar baixar; sem
  acesso ao resto do servidor.

Precedência: o que a pessoa respondeu > **regras do cliente** > a skill > regras gerais. Nunca usar travessão (—).

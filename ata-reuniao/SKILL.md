---
name: ata-reuniao
description: Transforma a transcrição de uma reunião na ATA completa no modelo da agência (7 seções) e separa as tarefas da agência para conferência.
---

# Gerar ATA da reunião

Você recebe a TRANSCRIÇÃO INTEIRA de uma reunião (feita por reconhecimento de voz: pode ter palavras erradas, nomes
trocados e falas sem identificação de quem fala), o cliente com as informações e as regras dele, o tipo da reunião e,
às vezes, quem participou. Entregue a ATA completa e as tarefas da agência.

## Regras de ouro

- A ATA é COMPLETA, nas 7 seções do modelo (referencias/modelo-ata.md), nunca um resumo da reunião.
- Nada inventado: tudo sai da transcrição. Se algo importante ficou ambíguo, escreva "(a confirmar)" no ponto e avise em
  "observacoes".
- Corrija o óbvio do reconhecimento de voz (nomes de produtos, do cliente e da agência, termos de marketing) pelo contexto.
- Tom: profissional, direto, frases curtas. Sem travessão (—): use hífen, vírgula ou dois pontos.
- Datas no formato DD/MM/AAAA. Prazos falados ("até sexta", "semana que vem") viram data a partir da data de hoje.
- Participantes: os informados; senão, os que dá para identificar pela conversa (nome e papel quando aparecer).

## As seções

1. **CONTEXTO**: por que a reunião aconteceu, em 2 a 4 linhas.
2. **O QUE FOI DISCUTIDO**: os assuntos, na ordem em que apareceram, um por linha, com o essencial de cada um
   (números, nomes, links e combinados citados).
3. **DECISÕES TOMADAS**: só o que foi decidido de fato (aprovado, escolhido, definido).
4. **TAREFAS DA AGÊNCIA**: o que a agência vai fazer, com prazo.
5. **TAREFAS DO CLIENTE**: o que o cliente vai fazer, com prazo (ficam só na ATA).
6. **PRÓXIMOS PASSOS**: próxima reunião (data/hora ou "a agendar") e outros encaminhamentos.
7. **NOVA DEMANDA / UPSELL**: se surgiu escopo novo ou oportunidade, descreva; senão "Nenhuma nesta reunião".

## O documento (campo "documento")

- `titulo`: `ATA - <CLIENTE> - <tipo> - <DD/MM/AAAA>`
- `markdown`: a ATA inteira, assim:

```
# ATA DE REUNIÃO

**Data:** DD/MM/AAAA
**Cliente:** <nome do cliente>
**Participantes:** <nomes>
**Tipo:** <tipo>

---

## 1. Contexto
...

## 2. O que foi discutido
- ...

## 3. Decisões tomadas
- ...

## 4. Tarefas da agência
- <tarefa>, prazo: DD/MM/AAAA

## 5. Tarefas do cliente
- <tarefa>, prazo: DD/MM/AAAA

## 6. Próximos passos
- Próxima reunião: ...

## 7. Nova demanda / upsell
...
```

## As tarefas (campo "tarefas")

- Uma tarefa para cada item da seção 4 (agência), com `lado` = "agencia". As da seção 5 também entram, com `lado` =
  "cliente" (aparecem desmarcadas: a pessoa decide se a agência acompanha).
- Título: `CLIENTE - descrição curta` (cliente em maiúsculas, sem emoji). Detalhes nas `notas`.
- Prazo: o dito na reunião; sem prazo dito, siga o POP: entrega ou follow-up em até 48h; próximo contato em 7 dias
  (5 para cliente tier amarelo); "quando der" fica null.
- `projeto_id`: o do cliente da reunião (outro cliente da lista só se a fala for claramente dele).
- `trecho`: um pedaço curto e literal da transcrição que originou a tarefa.
- `tipo` (prioridade): pela tabela da agência: entrega com prazo duro ou cliente esperando = prioridade alta;
  proposta/orçamento = dinheiro; relatório = relatório; acompanhamento = acompanhamento; o resto = execução.

## Resumo e observações

- `resumo`: 1 a 3 linhas do que foi a reunião e quantas tarefas saíram.
- `observacoes`: o que ficou "(a confirmar)", nomes que podem estar errados, e se a próxima reunião não ficou marcada.

---
name: extrator-tarefas
description: Extrai da transcrição de uma reunião as ações combinadas, como tarefas sugeridas para a pessoa conferir antes de criar.
---

# Extrair tarefas da reunião

A transcrição foi feita por reconhecimento de voz: pode ter palavras erradas e falas sem identificação de quem fala.

## Como extrair

- Uma tarefa por entrega ou ação concreta combinada. Junte o que é a mesma ação; não repita. Não invente nada que não
  foi dito.
- Ignore conversa social, explicações sem ação e o que já foi feito. Inclua decisões que geram trabalho e pedidos do
  cliente.
- Título curto no padrão `CLIENTE - descrição` (cliente em maiúsculas, sem emoji: a prioridade vai no campo `tipo`).
  Subitens e detalhes vão nas notas.
- Notas úteis para quem vai executar sem ter ouvido a reunião: o que fazer, contexto, números, nomes, links e combinados
  citados.
- Cliente (`projeto_id`): por padrão o cliente da reunião. Use outro da lista só quando a fala é claramente sobre outro
  cliente. Sem cliente da reunião, descubra pelo conteúdo (null se não der para saber).
- Responsável: só se uma pessoa da equipe foi citada como quem faz; senão null (fica com quem cria).
- Prazo: converta datas faladas ("até sexta", "semana que vem", "dia 20") para AAAA-MM-DD a partir de hoje. Sem prazo
  dito: entrega ou follow-up em até 48h; próximo contato em 7 dias (5 para tier amarelo); "quando der" fica null.
- `lado` = "cliente" para o que o CLIENTE ficou de fazer (vem desmarcado; a agência pode acompanhar).
- `trecho`: um pedaço curto e literal da transcrição que originou a tarefa.
- Prioridade (`tipo`): problema ativo = urgente; proposta/orçamento = dinheiro; prazo duro ou cliente esperando =
  prioridade; criativos do dia = criativo; acompanhamento/check-in = acompanhamento; relatório = relatório;
  administrativo = interno; "quando der" = quando_der; o resto = execução.
- Nunca use travessão (—).

## Resumo

`resumo`: 3 a 6 linhas: o assunto da reunião, as decisões e os próximos passos.

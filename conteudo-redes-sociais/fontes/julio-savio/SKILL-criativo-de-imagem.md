# Skill - Criativo de Imagem (by Julio Sávio)

Fonte: Google Drive, arquivo `Skill - Criativo de Imagem - by Julio Sávio.txt`, copiado para o brain em 22/09/2026. Se o Julio atualizar o original no Drive, atualizar esta cópia também, para as duas fontes não divergirem.

## Uso no brain

Esta skill é a base para montar o **prompt de geração de imagem** dos criativos estáticos de cliente. No formato original, ela é de **anúncio pago (ADS)**. Em **Social Media, que é sempre orgânico** (R17), ela é usada com os ajustes abaixo. Ver [`skills/Metodologia - Planejamento de Conteúdo Estático (Social Media).md`](Metodologia%20-%20Planejamento%20de%20Conte%C3%BAdo%20Est%C3%A1tico%20%28Social%20Media%29.md) para como este prompt se encaixa na estrutura de pasta do planejamento semestral/anual.

A skill original foi escrita para lote de 6 criativos de tráfego pago (Meta ADS). O lote de 6 (3 quadrado + 3 vertical) só se aplica a anúncio pago, nunca a Social Media.

Em **Social Media (sempre orgânico)**, a metodologia ajusta esta skill (e o ajuste prevalece sobre o texto original abaixo):

- **1 criativo por semana em 2 modelos** (A e B) com o mesmo texto e designs totalmente diferentes, cada um seguindo uma referência sorteada de `_Referências de design/` (2 famílias de layout, cena e cor dominante diferentes). Na mesa, cliente com imagens na aba Referências visuais tem nelas a direção de arte (diagramação, tipografia, fundo, grafismos), uma referência por modelo; sem elas, a diagramação vem de um template de `brain/templates/artes/` e a referência do Drive dá só o tipo de foto e o clima. Carrossel com no máximo 4 slides.
- **Arte sem logo e só com headline e subheadline.** Sem logo (o arquivo do logo entra só para extrair a paleta de cores), sem tag de cidade, sem botão de CTA, sem listas: cidade, CTA e detalhes vão na legenda. O logo no canto, a tag de cidade e o botão abaixo valem só para anúncio pago.
- O prompt é executado pelo **Codex na pasta `Social Media`**, lendo as referências (e o logo, só como paleta) pelos caminhos e salvando em `arte final/` da semana. Texto-base em [`skills/modelo-prompt-imagem.md`](modelo-prompt-imagem.md).

Em todos os casos, adaptar ao cliente do pedido: logo, cores e cidade são sempre do cliente atual, nunca genéricos nem da agência (ver `design-system.md` do cliente em `skills/regras-operacionais.md`).

**Importante:** quem gera a imagem a partir do arquivo `[prompt de imagem]` é o ChatGPT, não o Claude. O papel do Claude aqui é só escrever o prompt (texto), nunca gerar a imagem em si. Por isso o prompt deve ser autossuficiente e descritivo o bastante para funcionar colado direto no ChatGPT, sem depender de contexto que só o Claude teria (ex: não referenciar arquivos do brain, IDs internos ou instruções que fazem sentido só para o Claude).

---

## Texto original da skill (verbatim)

Skill - Criativo de Imagem

Preciso que você crie 6 criativos em imagens, sendo 3 no tamanho quadrado 1080x1080 e 3 no tamanho vertical 1080x1920, serão estritamente esses 2 únicos tamanhos de acordo com o que eu te solicitar abaixo. Sendo um criativo por imagem, nada de criar 6 criativos em uma única imagem, preciso de 6 imagens.

Esses criativos serão utilizados em tráfego pago no Meta ADS e devem ser persuasivos e usarem argumentos para fazer o cliente clicar no botão.

Cada criativo deve ser diferente um do outro, cada um deve abordar um ângulo de vista diferente e benefícios diferentes, com imagem diferente, headline diferente e conteúdo diferente, também deve variar o design.

Os 6 Criativos divulgam um mesmo serviço ou produto, porém cada criativo tem um ângulo diferente e/ou uma forma diferente de apresentar a proposta.

É obrigatório :

- Headline persuasiva
- Cidade onde será veiculado o anúncio - Quando o anúncio é veiculado em uma cidade local, deve colocar uma Tag ou escrito com o nome da cidade, por exemplo : Em São Paulo, Em Curitiba, quando essa informação não constar na headline, se tiver algo relacionada a cidade na headline não coloque isso.
- Ter o logo do cliente posicionado em um dos cantos
- Um elemento de continuidade ou grafismo de apoio. Mas a imagem não pode se repetir, cada página deve ter uma imagem diferente da outra.
- As cores devem seguir as cores da marca/logo.
- A fonte utilizada nos textos deve ser sempre Open Sons, você ajusta se quer deixar bold, normal, medium, etc… de acordo com o que ficar melhor em cada posicionamento.
- Você deve gerar uma imagem para cada criativo e não uma única imagem para todos os criativos.
- Um botão de CTA
- Depois que todas imagens forem criadas, conferir a ortografia para ver se não tem erros.

Tomar cuidado com :

- O Logo não pode ficar distorcido.
- Ao adicionar ícones e desenhos ou 2 imagens ao mesmo tempo nas páginas, as vezes fica confuso o excesso de informação, você deve adicionar muitos ícones e imagens quando isso é um tópico ou quando realmente faça sentido.
- Não gosto quando adiciona um ícone solto no canto da imagem sem nenhuma informação junto, não faça isso, use os ícones e desenhos de forma estratégica.
- Coloque somente a tag de cidade onde será veiculada o anúncio se for um anúncio específico para alguma cidade, se for a nivel brasil ou múltiplas cidade ou estados não coloque, na maioria das vezes eu vou te falar se é para uma região especifica.

Abaixo está o conteúdo de base para o criativo :

*(esta última linha marca onde, no uso original, entra o briefing específico do cliente/produto/oferta daquele criativo. No brain, esse conteúdo de base é o que muda a cada arquivo `[prompt de imagem]` gerado: produto, oferta, ângulo e prova daquela semana, extraídos do briefing do cliente, nunca inventados.)*

---
name: orquestrador-pipeline-sopro-de-fe
description: Skill gestora da rotina diária do canal Sopro de Fé. Coordena, em ordem, extração da mensagem do dia seguinte no PDF semanal, prompts musicais (Suno/Onlymusic), imagens no Codex, título, capinhas no ChatGPT e descrição do YouTube, salvando o pacote do dia. Use quando o usuário pedir "gerar o conteúdo", "rodar o pipeline", "conteúdo de amanhã" ou o conteúdo de um dia específico do Sopro de Fé.
---

# Orquestrador do Pipeline Diário: Sopro de Fé

Você coordena as skills das etapas e **para nos pontos que dependem do usuário**. Nunca pule uma parada, nunca invente conteúdo e nunca altere a letra. Responda em português.

## Pastas e arquivos (fixos)

- Base: `C:\Users\djava\Downloads\sopro-fe`
- PDF semanal: o **PDF mais recente na raiz da base** (o usuário o coloca lá).
- Imagens do Codex: `<base>\<dia>-feira-capitulos-1-4-vN\` (Etapa 3).
- Capinhas: `<base>\Thumbs\` (Etapa 4).
- **Pacote do dia:** `<base>\Textos\Msg<N>-<dia>\` com `saida_a.txt`, `saida_b.txt`, `style_prompt.txt`, `lyrics_prompt.txt`, `whatsapp.txt` (texto fixo, idêntico todo dia, vem de `scripts/whatsapp_template.txt` e é criado pelo `preparar_dia.py`; não reescreva nem altere o conteúdo), `meta.json`, `traducoes.txt` (espanhol neutro + inglês internacional, título e texto da Saída B) e, depois, `titulo.txt` e `descricao.txt`.

## Entrada do usuário

- "Gerar o conteúdo" → dia alvo = **amanhã** (D+1).
- "Gerar o de <dia>" → esse dia (`--dia quinta`).
- Se o usuário abrir um chat novo no meio do dia, **retome pelo pacote do dia**: veja quais arquivos já existem e continue da próxima etapa pendente (não refaça o que já está pronto).

## Fluxo

### Fase 1 (automática): extração + música
Invoque as skills `extrator-mensagem-diaria` e `gerador-prompts-musicais-sopro-de-fe` rodando o script que encadeia as duas e salva o pacote:

```bash
python -I "C:/Users/djava/.claude/skills/orquestrador-pipeline-sopro-de-fe/scripts/preparar_dia.py" [--dia quinta]
```

- Código 3 por **domingo**: o D+1 é a segunda da próxima mensagem. Peça o PDF novo (ou o dia específico).
- Código 3 por **sem PDF**: peça para colocar o PDF em `sopro-fe`.
- Aviso de **PDF antigo** (>8 dias): confirme se é a mensagem certa antes de seguir.
- Se o pacote já existe, use-o (só refaça com `--forcar` se o usuário pedir).

Entregue, **cada um em bloco de código próprio e rotulado**, lendo dos arquivos do pacote: **Style Prompt**, **Lyrics Prompt** (para Suno/Onlymusic). Diga o dia e o número da mensagem em uma linha.

#### Traduções (ainda na Fase 1): `traducoes.txt`
Logo após o script, traduza a **Saída B** (`saida_b.txt`) para **espanhol** e **inglês** e salve em `traducoes.txt` no pacote do dia (se já existir, não refaça). Você mesmo traduz (não há script de tradução). Regras:
- **Espanhol neutro/internacional**, entendido em todos os países hispanofalantes: sem regionalismos, gírias, voseo nem *vosotros* (use *ustedes*), sem expressões típicas da Espanha ou da Catalunha nem de um país da América Latina em particular.
- **Inglês internacional** simples e claro: sem gírias, sem expressões idiomáticas regionais, sem grafias ou termos marcadamente americanos ou britânicos quando houver alternativa neutra.
- **Fidelidade total:** traduza tudo, sem resumir, acrescentar, omitir nem interpretar; mantenha os 4 parágrafos na mesma ordem e a pontuação/aspas. Mantenha a capitalização dos pronomes que se referem a Deus como no original (Ele/Seu → Él/Su; He/His). Sem números de tópico e sem referências bíblicas (a Saída B não os tem).
- **O título da música ainda não existe nesta fase** (ele é escolhido na PARADA 2). Por isso, salve já o texto com o marcador `Título: (a definir)` / `Title: (to be defined)` e, **assim que o título for salvo em `titulo.txt`, traduza-o e preencha** os dois campos (mesmas regras, mantendo a palavra-chave em MAIÚSCULAS se o título original a tiver). Se o usuário já informar o título, use-o direto.
- Formato do arquivo:

```
=== ESPAÑOL (neutro) ===
Título: <título em espanhol>

<parágrafo 1>

<parágrafo 2>

<parágrafo 3>

<parágrafo 4>

=== ENGLISH (international) ===
Title: <title in English>

<paragraph 1>
...
```
- Avise em uma linha que `traducoes.txt` foi salvo. Não é necessário colar o conteúdo no chat, a menos que o usuário peça.

### PARADA 1: Codex (imagens)
Invoque `gerador-imagens-sopro-de-fe`. Entregue a **Saída A** (de `saida_a.txt`) em bloco de código e peça para colar no projeto do Codex. Avise que a música pode ser gerada em paralelo enquanto o Codex trabalha. **Espere** o usuário dizer que terminou.

### Fase 2: conferir imagens
Rode a conferência de `gerador-imagens-sopro-de-fe` (`conferir_imagens.py --dia <dia>`). Se **INCOMPLETO** (arquivo faltando ou proporção trocada), liste os arquivos e **pare**: o usuário corrige no Codex. Só avance com 16/16 OK.

### PARADA 2: Título
Invoque `gerador-thumbnail-seo-sopro-de-fe` (Passo 1): sugira 3 a 5 títulos e **espere a escolha**. Salve o escolhido, exatamente como escrito, em `titulo.txt` no pacote. Esse título vale para música, capinha e vídeo. Em seguida, traduza-o para espanhol neutro e inglês internacional e preencha os campos de título de `traducoes.txt` (ver "Traduções" na Fase 1).

### PARADA 3: Capinha (ChatGPT)
Ainda na skill de thumbnail (Passos 2 e 3): recomende a cena 16:9 com mais aderência ao título e dê a instrução para o ChatGPT (anexar imagem, enviar só o título, depois "Defina a proporção para 1:1"). **Espere** o usuário dizer que gerou e baixou as duas versões, então rode `organizar_thumbs.py --titulo "<Título>"` (Passo 4). Se faltar uma versão, avise.

### Fase 4 (automática): descrição
Passo 5 da skill de thumbnail: escolha 4 a 8 hashtags temáticas (as fixas `#ivpt #biblia #devocional` o script já põe), rode `montar_descricao.py` com `--dia <dia>`, salve em `descricao.txt` do pacote e entregue em bloco de código junto com o título do vídeo.

### Fechamento: checklist do Canva (manual)
O Canva é **manual**: o usuário sobe música e imagens no projeto `DAHOvg0P-0M` e ajusta a timeline pela duração dos versos e imagens. Não tente enviar nada ao Canva. Entregue uma lista curta:
- Música: baixar da plataforma o áudio final.
- 16 imagens: caminho da pasta `<dia>-feira-capitulos-1-4-vN`.
- Capinhas: `Thumbs\<Título>-16x09` e `-1x1`.
- Textos prontos em: caminho do pacote do dia (inclui `traducoes.txt`, com espanhol e inglês, e `whatsapp.txt`, a mensagem fixa do grupo do WhatsApp).

## Premissas adicionais (definidas pelo usuário em 2026-11-20)

- **Música:** no máximo 4 minutos, se possível; encerramento instrumental/solo de no máximo 20 s (já embutido em `gerador-prompts-musicais-sopro-de-fe`).
- **Conferência de imagens:** a correção de nomes (proporção + presença de texto) é parte da verificação, mas só com **autorização explícita do usuário a cada geração**: proponha a tabela de renomeação, pergunte e aguarde (ver `gerador-imagens-sopro-de-fe`). Verifique **os 4 capítulos**, mesmo que o script só acuse alguns.
- **whatsapp.txt:** todo pacote do dia inclui esse texto fixo. Se um pacote antigo não o tiver, o `preparar_dia.py` o cria sem refazer o resto.

## Regras gerais

- A letra é a Saída B sem nenhuma alteração; a conferência automática precisa ter passado.
- Nunca representar o rosto de Jesus nem a figura física de Deus nas imagens; se uma imagem violar, avise.
- Se um script falhar, mostre a mensagem de erro real e pare; não improvise o resultado.
- Seja breve entre as paradas: diga o que foi feito, o que aguarda o usuário e o próximo passo.

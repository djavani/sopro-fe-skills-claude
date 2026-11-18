---
name: gerador-thumbnail-seo-sopro-de-fe
description: Etapa 4 do pipeline Sopro de Fé. Sugere o título do dia (o mesmo da música e do vídeo), escolhe a cena limpa 16:9 com mais aderência ao título para a capinha, orienta a geração das capinhas 16:9 e 1:1 no ChatGPT, recolhe os arquivos para Downloads\sopro-fe\Thumbs e monta a descrição do YouTube no padrão do canal. Use após as imagens do dia estarem prontas, ou quando o usuário pedir título, capinha ou descrição do Sopro de Fé.
---

# Capinha e Publicação (Etapa 4)

Entradas: Saída A (Etapa 1), pasta de imagens do dia (Etapa 3, `Downloads\sopro-fe\<dia>-feira-capitulos-1-4-vN`).
O **título do vídeo é o mesmo título da música**. A capinha é gerada pelo usuário no ChatGPT (chat de memória "Novas Tumbs", com as premissas de identidade visual já salvas), não por esta skill.

## Passo 1: Título

Sugira 3 a 5 opções com base nos 4 tópicos do dia. Padrão do canal, observado nos títulos já usados:
- 2 a 4 palavras; **a palavra-chave em MAIÚSCULAS** (ex.: "Sangue que UNE", "Morte e VIDA", "O Caminho do ALTAR", "Festa das PRIMÍCIAS");
- direto, devocional, com acentuação correta; sem ponto final.
O usuário escolhe (ou dá o seu). **Escreva o título exatamente como escolhido**: ele precisa sair idêntico na capinha, no vídeo e na música.

## Passo 2: Escolher a cena da capinha

A cena é a que tem **mais aderência ao título**, e varia a cada dia. Abra (com Read) as 4 imagens `Capitulo-N-16x09.png` da pasta do dia e recomende uma, dizendo em uma frase por que combina com o título. Antes, confirme com `gerador-imagens-sopro-de-fe` (`conferir_imagens.py`) que o arquivo escolhido realmente é 16:9; já houve imagens quadradas com nome 16x09. Se o arquivo escolhido estiver com formato trocado, escolha outra ou peça ao usuário para regerar.

## Passo 3: Instrução para o ChatGPT

Diga ao usuário, curto e pronto para usar:
1. Anexar `<caminho completo da imagem escolhida>`.
2. Enviar **somente o título**, nesta forma exata: `<Título>`.
3. Depois que sair a capa 16:9, enviar: `Defina a proporção para 1:1`.
(O estilo, a tipografia metálica 3D dourada sobre pincelada vermelha e a regra de nunca mostrar o rosto de Jesus já estão nas premissas salvas no chat.)

## Passo 4: Recolher as capinhas

Quando o usuário disser que gerou e baixou as duas versões:

```bash
python -I "<pasta-da-skill>/scripts/organizar_thumbs.py" --titulo "<Título>"
```

O script procura na raiz de `Downloads` (arquivos dos últimos 3 dias cujo nome começa com o título), **classifica pela proporção real** (o ChatGPT acrescenta descrição ao nome, ex.: "Imerso na Palavra sob a Cachoeira.png") e **copia** para `Downloads\sopro-fe\Thumbs\<Título>-16x09.png` e `<Título>-1x1.png`. Não move nem apaga originais e não sobrescreve sem `--forcar`. Se avisar de vários candidatos, mostre ao usuário qual foi usado. Códigos: 0 ok, 2 falta uma versão, 3 nada encontrado.

## Passo 5: Descrição do YouTube

Salve a Saída A em arquivo e rode:

```bash
python -I "<pasta-da-skill>/scripts/montar_descricao.py" "<arquivo-saida-a.txt>" --hashtags "#tema1 #tema2 #tema3"   # dia = D+1 pela data do sistema
python -I "<pasta-da-skill>/scripts/montar_descricao.py" "<arquivo-saida-a.txt>" --dia quinta --hashtags "..."
```

Formato fixo (idêntico ao vídeo "Imerso na Palavra"): bloco do canal, linha em branco, **dia da semana** (`Quinta-Feira`), linha em branco, **Saída A íntegra** (4 tópicos numerados com referências bíblicas), linha em branco e a **linha de hashtags**. Entregue em um bloco de código para colar. Título do vídeo: o título do Passo 1. Não invente texto além disso.

**Hashtags (última linha da descrição):**
- Fixas, sempre primeiro (o YouTube mostra as 3 primeiras acima do título): `#ivpt #biblia #devocional`.
- Acrescente **4 a 8 hashtags temáticas** com aderência aos 4 tópicos e ao título do dia, passadas ao script em `--hashtags "#imersao #palavra ..."`. Estilo do canal: minúsculas, sem acento, sem espaço (como `#biblia`). Prefira termos que o público realmente busca (ex.: `#palavradedeus`, `#transformacao`, `#novohomem`, `#tabernaculo`, `#exodo`) e evite genéricas demais ou sem relação com o texto.
- O script remove duplicatas e limita a 15 no total (acima disso o YouTube ignora todas as hashtags).
- Mostre ao usuário a lista temática escolhida em uma linha, para ele poder trocar alguma.

## Entrega final do dia

Em poucas linhas: título escolhido, cena usada, caminhos das duas capinhas em `Thumbs`, e a descrição em bloco de código.

## Pendente (a combinar com o usuário)

**Canva: fica MANUAL por decisão do usuário.** Ele sobe a música e as imagens no projeto e ajusta a timeline conforme a duração dos versos e das imagens (design oficial `DAHOvg0P-0M`). Não tente enviar nada ao Canva; apenas liste, ao final do dia, os arquivos que ele vai subir (música a ser baixada da plataforma, 16 imagens do dia, capinhas em `Thumbs`).

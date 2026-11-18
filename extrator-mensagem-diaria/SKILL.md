---
name: extrator-mensagem-diaria
description: Etapa 1 do pipeline Sopro de Fé. Lê o PDF semanal "Imersão Ultrarrefinada na Palavra Profética", isola os 4 tópicos do dia seguinte (D+1) e gera a Saída A (íntegra, com numeração e versículos) e a Saída B (limpa, sem numeração nem referências bíblicas). Use quando o usuário enviar o PDF semanal, pedir a mensagem de amanhã, ou iniciar a rotina diária do Sopro de Fé.
---

# Extrator de Mensagem Diária (Etapa 1)

Entrada: caminho do PDF semanal. Saída: **Saída A** e **Saída B** do dia seguinte ao atual.

## Como executar

Rode sempre o script (não extraia de cabeça, o PDF tem quebras de linha dentro das referências):

```bash
python -I "<pasta-da-skill>/scripts/extrair.py" "<caminho-do-pdf>"
```

Opções: `--data AAAA-MM-DD` (simula "hoje") e `--dia-alvo quinta` (força o dia). Requer `pip install pypdf`.

O script calcula o D+1 pela data do sistema, localiza a página do dia (títulos `SEGUNDA-FEIRA` … `DOMINGO`), ignora cabeçalho, instruções, minutagem e o bloco "EXTRAIA DO TEXTO ACIMA…", e imprime `DIA_ALVO`, `===SAIDA_A===` e `===SAIDA_B===`.

## Formato da entrega (decidido com o usuário)

- **Sem cabeçalho nenhum** nas saídas: nem dia da semana, nem título da mensagem. Só o texto.
- **Saída A:** 4 parágrafos separados por linha em branco, mantendo `1.` a `4.` e as referências entre parênteses, exatamente como no PDF.
- **Saída B:** 4 parágrafos separados por linha em branco, **sem número e sem referências bíblicas**. Texto 100% preservado nas demais palavras, pontuação e perguntas.
- Apresente cada saída em seu próprio bloco de código, rotulado "Saída A" e "Saída B", para facilitar a cópia. Diga apenas em uma linha qual dia foi extraído.

## Casos especiais

- **Código de saída 3 (hoje é domingo):** o D+1 é a segunda-feira da *próxima* mensagem, que está em outro PDF. Peça o PDF novo; não use a segunda do PDF atual, a menos que o usuário peça (`--dia-alvo segunda`).
- **Código de saída 2:** seção do dia não encontrada ou diferente de 4 tópicos. Informe o erro e peça confirmação; não invente texto.
- Se o script avisar que sobrou algo parecido com referência na Saída B, revise o trecho manualmente e corrija sem alterar o resto.

## Passo seguinte

A Saída B segue intocada para `gerador-prompts-musicais-sopro-de-fe` (Etapa 2) e a Saída A para `gerador-imagens-sopro-de-fe` (Etapa 3).

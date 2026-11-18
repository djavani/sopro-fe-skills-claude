---
name: gerador-imagens-sopro-de-fe
description: Etapa 3 do pipeline Sopro de Fé. Entrega a Saída A (4 tópicos com numeração e versículos) para o usuário colar no projeto do Codex, que gera as 16 imagens (4 capítulos x 16x09/1x1, com e sem texto), e depois confere a pasta Downloads\sopro-fe do dia (arquivos presentes e proporções corretas). Use após a extração da mensagem diária, quando o usuário disser que as imagens foram geradas, ou ao pedir a conferência das imagens do Sopro de Fé.
---

# Gerador de Imagens (Etapa 3)

As premissas visuais (estilo cinematográfico, regras doutrinárias, nomes e pastas) **já estão no projeto do Codex do usuário**. Esta skill **não escreve prompts de imagem**: ela entrega a Saída A e confere o resultado.

## Fluxo

1. **Entregar a Saída A.** Use a Saída A produzida pela Etapa 1 (`extrator-mensagem-diaria`), sem cabeçalho, num bloco de código para copiar. Peça que o usuário cole no projeto do Codex. Se o Codex mostrar o plano das 4 cenas e pedir confirmação, é o usuário quem responde lá.
2. **Aguardar** o usuário dizer que o Codex terminou.
3. **Conferir a pasta do dia:**

```bash
python -I "<pasta-da-skill>/scripts/conferir_imagens.py"            # alvo = D+1 pela data do sistema
python -I "<pasta-da-skill>/scripts/conferir_imagens.py" --dia quinta   # forçar o dia
```

## O que o conferidor verifica

- Pasta `C:\Users\djava\Downloads\sopro-fe\<dia>-feira-capitulos-1-4-vN` (usa a maior versão `N`; opção `--base` muda a pasta raiz).
- 16 arquivos: `Capitulo-{1..4}-{16x09-com-texto, 16x09, 1x1-com-texto, 1x1}.png`.
- **Proporção real** de cada PNG: `16x09` deve ser ~1,78 e `1x1` deve ser 1,00. Isso importa porque a Etapa 4 usa `Capitulo-N-16x09.png` como base da capinha.
- Avisa se a pasta tem mais de 2 dias (pode ser da semana passada).

Códigos de saída: 0 ok, 2 incompleto/proporção errada, 3 pasta do dia não encontrada.

## Como reagir ao resultado

- **STATUS OK:** informe em uma linha e liste as 4 candidatas de capinha (16x09 limpas). Siga para a Etapa 4.
- **INCOMPLETO:** liste exatamente os arquivos com problema. **Não siga para a Etapa 4** com esses arquivos. Não renomeie nem apague nada do usuário. Sugira pedir ao Codex para regerar apenas os arquivos listados com a proporção correta.
  - Atenção: já ocorreu de o Codex salvar imagem quadrada com nome `16x09` (e vice-versa). Trocar nomes automaticamente é arriscado, pois pode misturar com/sem texto; confirme visualmente com o usuário antes de qualquer renomeação.
- **Pasta não encontrada (código 3):** as imagens ainda não foram geradas; lembre o usuário do passo 1.

## Regras que valem para as imagens (conferir ao olhar uma imagem, se o usuário pedir revisão)

- Cada capítulo tem uma cena coesa e única, coerente com o tópico.
- Proibido representar o rosto de Jesus ou a figura física de Deus.
- Versões com texto: texto integral do tópico; versões limpas: sem nenhum texto.

## Passo seguinte

`gerador-thumbnail-seo-sopro-de-fe` (Etapa 4) usa as imagens limpas 16x09 e a Saída A.

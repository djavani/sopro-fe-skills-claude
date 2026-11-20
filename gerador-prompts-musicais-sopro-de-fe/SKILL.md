---
name: gerador-prompts-musicais-sopro-de-fe
description: Etapa 2 do pipeline Sopro de Fé. Recebe a Saída B (4 parágrafos limpos do devocional do dia) e entrega o Style Prompt e o Lyrics Prompt com tags vocais e instrumentais entre colchetes, prontos para colar no Suno AI ou Onlymusic.ai. A letra é exatamente o texto, sem rimas, refrão, repetição ou alteração de qualquer palavra. Use após a extração da mensagem diária ou quando o usuário pedir o prompt/letra da música do Sopro de Fé.
---

# Gerador de Prompts Musicais (Etapa 2)

Entrada: **Saída B** (4 parágrafos separados por linha em branco, sem numeração e sem referências bíblicas).
Saída: **Style Prompt** + **Lyrics Prompt**.

## Regra de ouro

A música é um devocional cantado: **a letra é 100% o texto da Saída B**. Nunca criar rimas, refrão, repetições, resumos, cortes, trocas de palavra ou pontuação. Só se acrescentam as tags entre colchetes e os rótulos `Male Vocal` / `Female Vocal` do Bridge.

## Premissas de duração (fixas)

- A música deve ter **no máximo 4 minutos, se possível** (o Style Prompt pede "under 4 minutes, compact arrangement").
- O **encerramento** (`[Ending]`) é instrumental ou solo de **no máximo 20 segundos**, com fade out rápido. Não acrescentar nada depois dele.
- Se a plataforma gerar acima disso, avise o usuário para regenerar ou cortar o final.

## Como executar

Não monte a letra à mão. Salve a Saída B em um arquivo de texto UTF-8 e rode:

```bash
python -I "<pasta-da-skill>/scripts/gerar_prompts.py" "<arquivo-saida-b.txt>"
```

O script imprime `===STYLE===` e `===LYRICS===`, e **confere que as palavras da letra são idênticas às da Saída B** (se divergir, sai com erro 2: não entregue nada e avise o usuário).

## Estrutura fixa da letra

| Seção | Voz | Conteúdo |
|---|---|---|
| `[Intro]` | instrumental | sem letra |
| `[Verse 1]` | masculina | tópico 1 inteiro |
| `[Verse 2]` | feminina | tópico 2 inteiro |
| `[Bridge]` | masculina alternando com feminina | tópico 3 dividido ao meio por frases: 1ª metade em `Male Vocal`, 2ª em `Female Vocal` (número ímpar de frases: a masculina fica com a extra) |
| `[Interlude]` | instrumental | sem letra (solo de guitarra) |
| `[Final Section]` | dueto | tópico 4 inteiro |
| `[Ending]` | instrumental | sem letra, solo/outro de no máx. 20s, fade out rápido |

As tags (descrições instrumentais) e o Style Prompt estão fixos dentro do script, copiados do modelo que o usuário usa hoje. Para mudar o estilo, edite as constantes no topo de `gerar_prompts.py`.

## Formato da entrega

- Mostre **dois blocos de código separados**, rotulados "Style Prompt" e "Lyrics Prompt", para copiar e colar direto na plataforma.
- Sem comentários dentro dos blocos. Fora deles, no máximo uma linha dizendo que a conferência da letra passou.
- O Style Prompt tem cerca de 740 caracteres (cabe no limite de 1000 do Suno).

## Passo seguinte

A Saída A (com numeração e versículos) segue para `gerador-imagens-sopro-de-fe` (Etapa 3).

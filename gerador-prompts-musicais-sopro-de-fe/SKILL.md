---
name: gerador-prompts-musicais-sopro-de-fe
description: Etapa 2 do pipeline Sopro de Fé. Recebe a Saída B (4 parágrafos limpos do devocional do dia) e entrega o Style Prompt e o Lyrics Prompt com tags vocais e instrumentais entre colchetes, prontos para colar no Suno AI ou Onlymusic.ai. A letra é exatamente o texto, sem rimas, refrão, repetição ou alteração de qualquer palavra. Use após a extração da mensagem diária ou quando o usuário pedir o prompt/letra da música do Sopro de Fé.
---

# Gerador de Prompts Musicais (Etapa 2)

Entrada: **Saída B** (4 parágrafos separados por linha em branco, sem numeração e sem referências bíblicas).
Saída: **Style Prompt** + **Lyrics Prompt**.

## Regra de ouro

A música é um devocional cantado: **a letra é 100% o texto da Saída B**. Nunca criar rimas, refrão, repetições, resumos, cortes, trocas de palavra ou pontuação. Só se acrescentam as tags entre colchetes.

## Premissas de duração (fixas)

- A música deve ter **no máximo 4 minutos, se possível** (o Style Prompt pede "concise song structure").
- O **encerramento** (`[Short Outro]`) é um outro instrumental curto, **de no máximo 20 segundos**, com fade out limpo e `[End]`. Não acrescentar nada depois dele. (Estilo atualizado em 2026-11-24: balada pop suave, 82 BPM.)
- Se a plataforma gerar acima disso, avise o usuário para regenerar ou cortar o final.

## Como executar

Não monte a letra à mão. Salve a Saída B em um arquivo de texto UTF-8 e rode:

```bash
python -I "<pasta-da-skill>/scripts/gerar_prompts.py" "<arquivo-saida-b.txt>"
```

O script imprime `===STYLE===` e `===LYRICS===`, e **confere que as palavras da letra são idênticas às da Saída B** (se divergir, sai com erro 2: não entregue nada e avise o usuário).

## Estrutura fixa da letra (atualizada em 2026-11-24)

| Seção | Conteúdo |
|---|---|
| `[Short Intro: Soft Piano and Acoustic Guitar - 10s]` | instrumental |
| `[Verse 1]` | tópico 1 inteiro |
| `[Verse 2]` | tópico 2 inteiro |
| `[Short Bridge: <instrumento(s)> - 10s]` | instrumental de 10s; **o instrumento varia a cada execução** (sorteio no script: piano, violão, violoncelo, flauta, violino, harpa, guitarra limpa ou combinações). Não é regra ser sempre piano solo |
| `[Verse 3]` | tópico 3 inteiro |
| `[Verse 4]` | tópico 4 inteiro |
| `[Short Outro: Brief Instrumental Fade Out - max 20s] [End]` | instrumental |

Sem rótulos de voz masculina/feminina. O Style Prompt e as tags estão fixos nas constantes no topo de `gerar_prompts.py` (inclusive a lista `BRIDGES` da ponte). Para mudar o estilo, edite essas constantes.

## Formato da entrega

- Mostre **dois blocos de código separados**, rotulados "Style Prompt" e "Lyrics Prompt", para copiar e colar direto na plataforma.
- Sem comentários dentro dos blocos. Fora deles, no máximo uma linha dizendo que a conferência da letra passou.
- O Style Prompt tem cerca de 300 caracteres (cabe no limite do Suno).

## Passo seguinte

A Saída A (com numeração e versículos) segue para `gerador-imagens-sopro-de-fe` (Etapa 3).

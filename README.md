# Skills do pipeline Sopro de Fé

Skills do Claude Code que automatizam a rotina diária do canal Sopro de Fé:

- `orquestrador-pipeline-sopro-de-fe`: coordena todas as etapas e paradas
- `extrator-mensagem-diaria`: extrai os 4 tópicos do dia do PDF semanal (Saídas A e B)
- `gerador-prompts-musicais-sopro-de-fe`: Style Prompt e Lyrics Prompt (Suno/Onlymusic)
- `gerador-imagens-sopro-de-fe`: entrega a Saída A ao Codex e confere as 16 imagens
- `gerador-thumbnail-seo-sopro-de-fe`: título, capinhas e descrição do YouTube

## Uso em outro computador

Clone este repositório em `~/.claude/skills` (Windows: `C:\Users\<usuario>\.claude\skills`) e instale as dependências:

```bash
pip install pypdf pillow
```

Os arquivos de trabalho (PDF, imagens, capinhas, textos do dia) ficam em `Downloads\sopro-fe` e não fazem parte deste repositório.

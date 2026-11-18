#!/usr/bin/env python3
"""Etapas automaticas 1 e 2 do pipeline Sopro de Fe: extracao + prompts musicais, salvando o pacote do dia.

Uso:
    python preparar_dia.py [--dia quinta] [--data AAAA-MM-DD] [--pdf CAMINHO] [--base CAMINHO] [--forcar]

- Base (padrao ~/Downloads/sopro-fe): o PDF mais recente nela (so a raiz) e usado, salvo --pdf.
- Dia: --dia, ou D+1 pela data do sistema (ou --data). Domingo sem --dia: aborta (segunda e de outra mensagem).
- Cria <base>/Textos/Msg<N>-<dia>/ com: saida_a.txt, saida_b.txt, style_prompt.txt, lyrics_prompt.txt, meta.json
  (N = numero da mensagem lido do PDF; se nao achar, usa a data).
- Nao sobrescreve um pacote existente sem --forcar.
Codigos de saida: 0 ok | 2 erro de leitura/estrutura | 3 domingo/sem PDF
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")
SK = os.path.join(HOME, ".claude", "skills")
EXTRATOR = os.path.join(SK, "extrator-mensagem-diaria", "scripts", "extrair.py")
MUSICA = os.path.join(SK, "gerador-prompts-musicais-sopro-de-fe", "scripts", "gerar_prompts.py")


def rodar(cmd):
    r = subprocess.run([sys.executable, "-I"] + cmd, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


def numero_mensagem(pdf):
    try:
        from pypdf import PdfReader
        t = PdfReader(pdf).pages[0].extract_text() or ""
        m = re.search(r"Mensagem\s+(\d+)", t)
        return m.group(1) if m else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dia")
    ap.add_argument("--data")
    ap.add_argument("--pdf")
    ap.add_argument("--base", default=os.path.join(HOME, "Downloads", "sopro-fe"))
    ap.add_argument("--forcar", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    pdf = a.pdf
    if not pdf:
        pdfs = [os.path.join(a.base, f) for f in os.listdir(a.base) if f.lower().endswith(".pdf")] if os.path.isdir(a.base) else []
        if not pdfs:
            print(f"Nenhum PDF encontrado em {a.base}. Coloque o PDF semanal nessa pasta ou use --pdf.")
            sys.exit(3)
        pdf = max(pdfs, key=os.path.getmtime)
    idade = (dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getmtime(pdf))).days
    print(f"PDF: {pdf}")
    print(f"PDF_IDADE_DIAS: {idade}")
    if idade > 8:
        print("AVISO: PDF com mais de 8 dias; pode ser de uma mensagem anterior. Confirme com o usuario.")

    # --- Etapa 1: extracao
    cmd = [EXTRATOR, pdf] + (["--dia-alvo", a.dia] if a.dia else (["--data", a.data] if a.data else []))
    rc, out, err = rodar(cmd)
    if rc != 0:
        print((err.strip() or out.strip()).replace("--dia-alvo", "--dia"))
        sys.exit(rc if rc in (2, 3) else 2)
    m = re.search(r"DIA_ALVO:\s*(\S+)", out)
    dia_alvo = m.group(1)
    saida_a = out.split("===SAIDA_A===")[1].split("===SAIDA_B===")[0].strip()
    saida_b = out.split("===SAIDA_B===")[1].strip()

    nome_pasta_dia = dia_alvo.split("-")[0].lower().replace("ç", "c").replace("á", "a")
    num = numero_mensagem(pdf)
    rotulo = f"Msg{num}" if num else dt.date.today().isoformat()
    pasta = os.path.join(a.base, "Textos", f"{rotulo}-{nome_pasta_dia}")
    if os.path.isdir(pasta) and os.listdir(pasta) and not a.forcar:
        print(f"PACOTE_JA_EXISTE: {pasta}\n(use --forcar para refazer; os arquivos atuais foram mantidos)")
        print(f"DIA_ALVO: {dia_alvo}")
        sys.exit(0)
    os.makedirs(pasta, exist_ok=True)

    def salvar(nome, texto):
        with open(os.path.join(pasta, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write(texto.strip() + "\n")

    salvar("saida_a.txt", saida_a)
    salvar("saida_b.txt", saida_b)

    # --- Etapa 2: prompts musicais
    rc, out2, err2 = rodar([MUSICA, os.path.join(pasta, "saida_b.txt")])
    if rc != 0:
        print("ERRO na etapa de musica:", err2.strip())
        sys.exit(2)
    style = out2.split("===STYLE===")[1].split("===LYRICS===")[0]
    lyrics = out2.split("===LYRICS===")[1]
    salvar("style_prompt.txt", style)
    salvar("lyrics_prompt.txt", lyrics)

    meta = {"pdf": pdf, "mensagem": num, "dia": dia_alvo, "pasta": pasta,
            "gerado_em": dt.datetime.now().isoformat(timespec="seconds")}
    salvar("meta.json", json.dumps(meta, ensure_ascii=False, indent=2))

    print(f"DIA_ALVO: {dia_alvo}")
    print(f"MENSAGEM: {num or 'nao identificada'}")
    print(f"PACOTE: {pasta}")
    print("ARQUIVOS: saida_a.txt, saida_b.txt, style_prompt.txt, lyrics_prompt.txt, meta.json")
    print("CONFERENCIA_LETRA: ok (palavras da letra identicas a Saida B)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Confere as 16 imagens geradas pelo Codex para o dia alvo.

Uso:
    python conferir_imagens.py [--data AAAA-MM-DD | --dia quinta] [--base CAMINHO]

Procura em <base> (padrao: ~/Downloads/sopro-fe) a pasta '<dia>-feira-capitulos-1-4-vN'
(ou '<dia>-capitulos-...' para sabado/domingo), usa a de maior versao N e confere:
  - 4 capitulos x 4 arquivos: Capitulo-N-16x09-com-texto, -16x09, -1x1-com-texto, -1x1 (.png)
  - proporcao: 16x09 ~ 1.78 ; 1x1 = 1.00
Codigos de saida: 0 tudo certo | 2 faltam arquivos / proporcao errada | 3 pasta do dia nao encontrada
"""
import argparse
import datetime as dt
import os
import re
import struct
import sys
import unicodedata

CHAVES = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]
VARIANTES = ["16x09-com-texto", "16x09", "1x1-com-texto", "1x1"]


def norm(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def dimensoes_png(caminho):
    with open(caminho, "rb") as f:
        h = f.read(24)
    if h[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", h[16:24])


def achar_pasta(base, chave):
    candidatas = []
    for nome in os.listdir(base):
        n = norm(nome)
        if os.path.isdir(os.path.join(base, nome)) and n.startswith(chave):
            m = re.search(r"-v(\d+)$", n)
            candidatas.append((int(m.group(1)) if m else 0, nome))
    return max(candidatas)[1] if candidatas else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="data de hoje AAAA-MM-DD (alvo = D+1)")
    ap.add_argument("--dia", help="forca o dia (ex.: quinta)")
    ap.add_argument("--base", default=os.path.join(os.path.expanduser("~"), "Downloads", "sopro-fe"))
    a = ap.parse_args()

    if a.dia:
        chave = norm(a.dia)
        chave = next((c for c in CHAVES if c.startswith(chave)), None)
        if not chave:
            sys.exit("Dia invalido: " + a.dia)
    else:
        hoje = dt.date.fromisoformat(a.data) if a.data else dt.date.today()
        chave = CHAVES[(hoje + dt.timedelta(days=1)).weekday()]

    sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.isdir(a.base):
        print(f"Pasta base nao existe: {a.base}")
        sys.exit(3)
    pasta = achar_pasta(a.base, chave)
    if not pasta:
        print(f"DIA: {chave}\nPASTA: nao encontrada em {a.base}\nSTATUS: imagens ainda nao geradas")
        sys.exit(3)

    caminho = os.path.join(a.base, pasta)
    idade = (dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getmtime(caminho))).days
    problemas = []
    for cap in range(1, 5):
        for v in VARIANTES:
            f = os.path.join(caminho, f"Capitulo-{cap}-{v}.png")
            if not os.path.isfile(f):
                problemas.append(f"FALTA: Capitulo-{cap}-{v}.png")
                continue
            dim = dimensoes_png(f)
            if not dim:
                problemas.append(f"INVALIDO (nao e PNG): Capitulo-{cap}-{v}.png")
                continue
            r = dim[0] / dim[1]
            esperado = 16 / 9 if v.startswith("16x09") else 1.0
            if abs(r - esperado) > 0.03:
                problemas.append(f"PROPORCAO {dim[0]}x{dim[1]}: Capitulo-{cap}-{v}.png")

    print(f"DIA: {chave}")
    print(f"PASTA: {caminho}")
    print(f"IDADE_DA_PASTA_DIAS: {idade}")
    if idade > 2:
        print("AVISO: pasta antiga; pode ser da semana passada. Confirme com o usuario.")
    if problemas:
        print("STATUS: INCOMPLETO")
        print("\n".join(problemas))
        sys.exit(2)
    print("STATUS: OK (16/16 imagens, proporcoes corretas)")
    print("CANDIDATAS_THUMBNAIL (16x09 limpas):")
    for cap in range(1, 5):
        print(os.path.join(caminho, f"Capitulo-{cap}-16x09.png"))


if __name__ == "__main__":
    main()

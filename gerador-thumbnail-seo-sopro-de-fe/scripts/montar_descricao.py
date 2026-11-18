#!/usr/bin/env python3
"""Monta a descricao do video no padrao do canal Sopro de Fe.

Uso:
    python montar_descricao.py <arquivo_saida_a.txt> [--dia quinta | --data AAAA-MM-DD] [--hashtags "#a #b"]

--dia   dia da semana da MENSAGEM (o alvo D+1 da Etapa 1)
--data  data de hoje; o dia usado e D+1 (padrao: hoje do sistema)
Entrada: Saida A (4 topicos numerados, com versiculos entre parenteses).
Saida: descricao pronta para colar no YouTube.
"""
import argparse
import datetime as dt
import re
import sys
import unicodedata

BLOCO_FIXO = (
    "Transcrição da Imersão da palavra profética, Instituto Vida para todos.\n"
    "Encorajamento e direção para avançar com o evangelho de Jesus na terra.\n"
    "\n"
    "Deus te abençoe\n"
    "\n"
    "Canal Oficial\n"
    "@institutovidaparatodos"
)

ROTULOS = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"]

# Hashtags fixas do canal: sempre as tres primeiras (o YouTube exibe as 3 primeiras acima do titulo).
HASHTAGS_FIXAS = ["#ivpt", "#biblia", "#devocional"]
MAX_HASHTAGS = 15  # acima disso o YouTube ignora todas


def montar_hashtags(extras):
    """Fixas + extras tematicas: minusculas, sem espaco, sem duplicata, limite de 15."""
    saida = list(HASHTAGS_FIXAS)
    for h in re.findall(r"#?[^\s#,;]+", extras or ""):
        h = "#" + h.lstrip("#").lower()
        if h not in saida:
            saida.append(h)
    return saida[:MAX_HASHTAGS]


def norm(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("saida_a")
    ap.add_argument("--dia")
    ap.add_argument("--data")
    ap.add_argument("--hashtags", default="", help='hashtags tematicas extras, ex.: "#imersao #palavra #transformacao"')
    a = ap.parse_args()

    if a.dia:
        k = norm(a.dia)
        idx = next((i for i, r in enumerate(ROTULOS) if norm(r).startswith(k)), None)
        if idx is None:
            sys.exit("Dia invalido: " + a.dia)
    else:
        hoje = dt.date.fromisoformat(a.data) if a.data else dt.date.today()
        idx = (hoje + dt.timedelta(days=1)).weekday()

    bruto = open(a.saida_a, encoding="utf-8").read()
    topicos = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", bruto.strip()) if p.strip()]
    if len(topicos) != 4 or not all(re.match(rf"^{n}\.\s", t) for n, t in enumerate(topicos, 1)):
        sys.stderr.write("Esperava a Saida A: 4 paragrafos numerados de 1. a 4. (com referencias).\n")
        sys.exit(2)

    descricao = (f"{BLOCO_FIXO}\n\n{ROTULOS[idx]}\n\n" + "\n\n".join(topicos)
                 + "\n\n" + " ".join(montar_hashtags(a.hashtags)))
    if len(descricao) > 5000:
        sys.stderr.write(f"AVISO: descricao com {len(descricao)} caracteres (limite do YouTube: 5000).\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(descricao)


if __name__ == "__main__":
    main()

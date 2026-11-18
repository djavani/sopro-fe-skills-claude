#!/usr/bin/env python3
"""Extrai os 4 topicos do dia seguinte (D+1) do PDF semanal 'Imersao Ultrarrefinada'.

Uso:
    python extrair.py <caminho_do_pdf> [--data AAAA-MM-DD] [--dia-alvo quinta]

Saida (stdout):
    ===SAIDA_A===   texto integro (numeracao + referencias biblicas)
    ===SAIDA_B===   texto limpo (sem numeracao, sem referencias)
Codigos de saida: 0 ok | 2 erro de leitura/estrutura | 3 D+1 cai em outra semana (domingo -> segunda)
"""
import argparse
import datetime as dt
import re
import sys
import unicodedata

DIAS = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA",
        "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.upper().strip()


def resolver_dia(args):
    if args.dia_alvo:
        chave = norm(args.dia_alvo)
        for i, d in enumerate(DIAS):
            if norm(d).startswith(chave):
                return i, None
        sys.exit("Dia alvo invalido: " + args.dia_alvo)
    hoje = dt.date.fromisoformat(args.data) if args.data else dt.date.today()
    alvo = hoje + dt.timedelta(days=1)
    return alvo.weekday(), (hoje, alvo)


def ler_paginas(caminho):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.stderr.write("Falta a biblioteca pypdf. Instale com: pip install pypdf\n")
        sys.exit(2)
    return [(p.extract_text() or "") for p in PdfReader(caminho).pages]


def achar_pagina(paginas, dia):
    alvo = norm(dia)
    for texto in paginas:
        for linha in texto.splitlines():
            if norm(linha) == alvo:
                return texto
    return None


def juntar(linhas):
    """Junta linhas quebradas. 'a:3-' + '4' vira 'a:3-4' (sem espaco)."""
    out = ""
    for l in linhas:
        l = l.strip()
        if not l:
            continue
        if not out:
            out = l
        elif re.search(r"\d-$", out) and re.match(r"\d", l):
            out += l
        else:
            out += " " + l
    return re.sub(r"\s+", " ", out).strip()


def extrair_topicos(pagina, dia):
    linhas = pagina.splitlines()
    ini = next(i for i, l in enumerate(linhas) if norm(l) == norm(dia))
    # pula a linha de minutagem "(Trecho de referencia ...)", que pode quebrar em varias linhas
    i = ini + 1
    while i < len(linhas) and not re.match(r"^\s*1\.\s", linhas[i]):
        i += 1
    topicos, atual = [], None
    for l in linhas[i:]:
        if norm(l).startswith("EXTRAIA DO TEXTO"):
            break
        m = re.match(r"^\s*([1-9])\.\s+(.*)", l)
        esperado = len(topicos) + (2 if atual is not None else 1)
        if m and int(m.group(1)) == esperado:
            if atual is not None:
                topicos.append(juntar(atual))
            atual = [m.group(2)]
        elif atual is not None:
            atual.append(l)
    if atual is not None:
        topicos.append(juntar(atual))
    return topicos


REF = re.compile(r"\s*\([^()]*\d+\s*:\s*\d+[^()]*\)")


def limpar(t):
    t = REF.sub("", t)
    t = re.sub(r"([?!])\.", r"\1", t)      # 'hoje?.' -> 'hoje?'
    t = re.sub(r"\s+([.,;:?!])", r"\1", t)  # espaco antes de pontuacao
    t = re.sub(r"(?<![.…])\.\.(?![.])", ".", t)  # 'elementos. (Ef 5:26).' -> 'elementos..' -> 'elementos.'
    return re.sub(r"\s+", " ", t).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--data", help="data de hoje AAAA-MM-DD (padrao: hoje)")
    ap.add_argument("--dia-alvo", help="forca o dia (ex.: quinta), ignora a data")
    args = ap.parse_args()

    idx, datas = resolver_dia(args)
    if datas and datas[0].weekday() == 6:  # hoje domingo -> amanha e segunda da proxima mensagem
        sys.stderr.write("AVISO: hoje e domingo; o D+1 (segunda-feira) pertence a PROXIMA mensagem. "
                         "Envie o PDF novo ou use --dia-alvo segunda para forcar.\n")
        sys.exit(3)
    dia = DIAS[idx]

    pagina = achar_pagina(ler_paginas(args.pdf), dia)
    if not pagina:
        sys.stderr.write(f"Secao '{dia}' nao encontrada no PDF.\n")
        sys.exit(2)
    topicos = extrair_topicos(pagina, dia)
    if len(topicos) != 4:
        sys.stderr.write(f"Esperava 4 topicos em '{dia}', encontrei {len(topicos)}.\n")
        sys.exit(2)

    saida_a = "\n\n".join(f"{n}. {t}" for n, t in enumerate(topicos, 1))
    limpos = [limpar(t) for t in topicos]
    saida_b = "\n\n".join(limpos)
    if re.search(r"\d+\s*:\s*\d+", saida_b):
        sys.stderr.write("AVISO: sobrou algo parecido com referencia biblica na Saida B; revise.\n")

    sys.stdout.reconfigure(encoding="utf-8")
    print(f"DIA_ALVO: {dia}")
    print("===SAIDA_A===")
    print(saida_a)
    print("===SAIDA_B===")
    print(saida_b)


if __name__ == "__main__":
    main()

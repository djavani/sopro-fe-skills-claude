#!/usr/bin/env python3
"""Recolhe as capinhas geradas pelo ChatGPT (na raiz de Downloads) para sopro-fe\\Thumbs.

Uso:
    python organizar_thumbs.py --titulo "Imerso na Palavra" [--dias 3] [--forcar]
                               [--origem CAMINHO] [--destino CAMINHO]

- Procura PNG/JPG/WEBP na ORIGEM (padrao ~/Downloads, so a raiz) cujo nome comece com o titulo
  (sem acentos, sem diferenciar maiusculas) e que tenham sido modificados nos ultimos --dias dias.
  O ChatGPT acrescenta descricao ao nome (ex.: 'Imerso na Palavra sob a Cachoeira.png'),
  por isso a classificacao e feita pela PROPORCAO REAL, nao pelo nome.
- 16:9 (~1,78) -> '<Titulo>-16x09.<ext>' ; 1:1 (~1,00) -> '<Titulo>-1x1.<ext>' em <destino> (padrao ~/Downloads/sopro-fe/Thumbs).
- COPIA (nao move nem apaga o original) e nao sobrescreve sem --forcar.
Codigos de saida: 0 as duas versoes ok | 2 falta alguma versao | 3 nenhum arquivo encontrado
"""
import argparse
import datetime as dt
import os
import re
import shutil
import struct
import sys
import unicodedata

EXTS = (".png", ".jpg", ".jpeg", ".webp")


def norm(s):
    s = unicodedata.normalize("NFD", s)
    return re.sub(r"\s+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn").lower()).strip()


def dimensoes(caminho):
    with open(caminho, "rb") as f:
        h = f.read(32)
        if h[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", h[16:24])
        if h[:4] == b"RIFF" and h[8:12] == b"WEBP":
            f.seek(0)
            d = f.read(40)
            if d[12:16] == b"VP8X":
                return (1 + int.from_bytes(d[24:27], "little"), 1 + int.from_bytes(d[27:30], "little"))
            return None
        if h[:2] == b"\xff\xd8":  # JPEG: procura marcador SOF
            f.seek(2)
            while True:
                m = f.read(2)
                if len(m) < 2 or m[0] != 0xFF:
                    return None
                ln = struct.unpack(">H", f.read(2))[0]
                if m[1] in (0xC0, 0xC1, 0xC2):
                    f.read(1)
                    hh, ww = struct.unpack(">HH", f.read(4))
                    return (ww, hh)
                f.seek(ln - 2, 1)
    return None


def formato(dim):
    if not dim:
        return None
    r = dim[0] / dim[1]
    if abs(r - 16 / 9) < 0.05:
        return "16x09"
    if abs(r - 1.0) < 0.03:
        return "1x1"
    return None


def main():
    home = os.path.expanduser("~")
    ap = argparse.ArgumentParser()
    ap.add_argument("--titulo", required=True)
    ap.add_argument("--dias", type=int, default=3)
    ap.add_argument("--forcar", action="store_true")
    ap.add_argument("--origem", default=os.path.join(home, "Downloads"))
    ap.add_argument("--destino", default=os.path.join(home, "Downloads", "sopro-fe", "Thumbs"))
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    t = norm(a.titulo)
    limite = dt.datetime.now() - dt.timedelta(days=a.dias)
    achados = {"16x09": [], "1x1": []}
    ignorados = []
    for nome in os.listdir(a.origem):
        base, ext = os.path.splitext(nome)
        caminho = os.path.join(a.origem, nome)
        if ext.lower() not in EXTS or not os.path.isfile(caminho) or not norm(base).startswith(t):
            continue
        mt = dt.datetime.fromtimestamp(os.path.getmtime(caminho))
        if mt < limite:
            ignorados.append(f"{nome} (antigo: {mt:%d/%m})")
            continue
        fm = formato(dimensoes(caminho))
        if fm:
            achados[fm].append((mt, caminho))
        else:
            ignorados.append(f"{nome} (proporcao nao e 16:9 nem 1:1)")

    os.makedirs(a.destino, exist_ok=True)
    seguro = re.sub(r'[<>:"/\\|?*]', "", a.titulo).strip()
    faltando = []
    for fm in ("16x09", "1x1"):
        if not achados[fm]:
            faltando.append(fm)
            print(f"FALTA: versao {fm} de '{a.titulo}'")
            continue
        achados[fm].sort(reverse=True)  # mais recente primeiro
        mt, origem = achados[fm][0]
        ext = os.path.splitext(origem)[1].lower()
        alvo = os.path.join(a.destino, f"{seguro}-{fm}{ext}")
        if os.path.exists(alvo) and not a.forcar:
            print(f"JA EXISTE (nao sobrescrito): {alvo}")
        else:
            shutil.copy2(origem, alvo)
            print(f"COPIADO: {origem}\n     ->  {alvo}")
        if len(achados[fm]) > 1:
            print(f"AVISO: {len(achados[fm])} candidatos {fm}; usei o mais recente ({os.path.basename(origem)}). Outros:")
            for _, c in achados[fm][1:]:
                print("   -", os.path.basename(c))
    for i in ignorados:
        print("IGNORADO:", i)
    if not achados["16x09"] and not achados["1x1"]:
        sys.exit(3)
    sys.exit(2 if faltando else 0)


if __name__ == "__main__":
    main()

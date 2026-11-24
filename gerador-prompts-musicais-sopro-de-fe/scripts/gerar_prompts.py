#!/usr/bin/env python3
"""Monta o Style Prompt e o Lyrics Prompt (com tags) a partir da Saida B.

Uso:
    python gerar_prompts.py <arquivo_saida_b.txt>      (ou '-' para ler do stdin)

Entrada: 4 paragrafos separados por linha em branco (Saida B, sem numeracao nem referencias).
Saida:  ===STYLE===  e  ===LYRICS===
A letra e 100% o texto da Saida B: nada e adicionado, repetido, cortado ou reescrito.
O script confere isso no final (codigo de saida 2 se alguma palavra divergir).
"""
import random
import re
import sys

STYLE = (
    "soft pop ballad, smooth acoustic guitar fingerpicking, gentle upright piano chords, "
    "warm ambient synth pads, emotional soft vocal, mid-tempo 82 BPM, minimal instrumental interludes, "
    "short bridge, brief 15-20s instrumental outro, clean fade out, concise song structure, high fidelity mix"
)

TAG_INTRO = "[Short Intro: Soft Piano and Acoustic Guitar - 10s]"
TAG_ENDING = "[Short Outro: Brief Instrumental Fade Out - max 20s] [End]"

# A ponte instrumental (10s) varia a cada execucao: solos de varios instrumentos ou combinacoes.
BRIDGES = [
    "Minimal Piano Solo",
    "Soft Acoustic Guitar Solo",
    "Warm Cello Solo",
    "Gentle Flute Solo",
    "Delicate Violin Solo",
    "Soft Harp Arpeggios",
    "Clean Electric Guitar Solo with Subtle Delay",
    "Warm Cello and Acoustic Guitar Duet",
    "Piano and Violin Duet",
    "Flute and Harp with Soft Synth Pads",
    "Acoustic Guitar, Piano and Warm Cello Trio",
    "Soft Strings and Piano Ensemble",
]

# fim de frase: . ? ! (opcionalmente fechando aspas) seguido de espaco e inicio de nova frase
FIM_FRASE = re.compile(r"(?<=[.?!])\s+|(?<=[.?!][”\"])\s+")


def frases(texto):
    return [f.strip() for f in FIM_FRASE.split(texto.strip()) if f.strip()]


def montar(topicos):
    bridge = f"[Short Bridge: {random.choice(BRIDGES)} - 10s]"
    blocos = [
        TAG_INTRO,
        f"[Verse 1]\n{topicos[0]}",
        f"[Verse 2]\n{topicos[1]}",
        bridge,
        f"[Verse 3]\n{topicos[2]}",
        f"[Verse 4]\n{topicos[3]}",
        TAG_ENDING,
    ]
    return "\n\n".join(blocos)


def palavras(t):
    return re.findall(r"\S+", t)


def conferir(topicos, letra):
    """A letra, sem tags entre colchetes, deve ter exatamente as palavras da Saida B."""
    sem_tags = re.sub(r"\[[^\]]*\]", " ", letra)
    return palavras(sem_tags) == palavras(" ".join(topicos))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    bruto = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    topicos = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", bruto.strip()) if p.strip()]
    if len(topicos) != 4:
        sys.stderr.write(f"Esperava 4 paragrafos na Saida B, recebi {len(topicos)}.\n")
        sys.exit(2)
    if any(re.match(r"^\d\.\s", t) or re.search(r"\d+\s*:\s*\d+", t) for t in topicos):
        sys.stderr.write("A Saida B ainda tem numeracao ou referencia biblica; use a Saida B limpa.\n")
        sys.exit(2)
    letra = montar(topicos)
    if not conferir(topicos, letra):
        sys.stderr.write("ERRO: a letra montada nao confere com a Saida B.\n")
        sys.exit(2)
    sys.stdout.reconfigure(encoding="utf-8")
    print("===STYLE===")
    print(STYLE)
    print("===LYRICS===")
    print(letra)


if __name__ == "__main__":
    main()

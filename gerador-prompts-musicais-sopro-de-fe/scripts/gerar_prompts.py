#!/usr/bin/env python3
"""Monta o Style Prompt e o Lyrics Prompt (com tags) a partir da Saida B.

Uso:
    python gerar_prompts.py <arquivo_saida_b.txt>      (ou '-' para ler do stdin)

Entrada: 4 paragrafos separados por linha em branco (Saida B, sem numeracao nem referencias).
Saida:  ===STYLE===  e  ===LYRICS===
A letra e 100% o texto da Saida B: nada e adicionado, repetido, cortado ou reescrito.
O script confere isso no final (codigo de saida 2 se alguma palavra divergir).
"""
import re
import sys

STYLE = (
    "Modern Christian Devotional Pop-Rock Worship, contemporary gospel pop, 80 BPM, "
    "energetic acoustic guitars, electric guitar riffs and power chords, subtle delay, expressive guitar solo, "
    "driving bass, punchy live pop drums, powerful snare and bright cymbals, grand piano, warm cello, "
    "ambient synth pads, male and female duet with alternating emotional lead vocals, soft backing choir, "
    "uplifting prayerful and reverent atmosphere, dynamic instrumental build, "
    "powerful worship chorus and final section, full band arrangement, high-fidelity modern studio production, "
    "compact arrangement, under 4 minutes. Very short instrumental outro, maximum 20 seconds, brief final resolution, "
    "no extended solo or instrumental repetition after the final chorus, finish naturally and decisively."
)

TAG_INTRO = ("[Intro: 8s Modern Christian Pop-Rock, Energetic Acoustic Guitar Strumming, Electric Guitar Power Chords "
             "with Subtle Delay, Melodic Electric Guitar Riffs, Driving Electric Bass, Punchy Live Pop-Rock Drums, "
             "Bright Cymbal Hits, Ambient Synth Pads, Grand Piano Accents - Strong Rhythmic Build, Fast Vocal Entry]")
TAG_V1 = ("[Verse 1: Male Vocal - Warm Modern Pop-Rock, Rhythmic Acoustic Guitar, Clean Electric Guitar, "
          "Deep Electric Bass, Steady Live Drums]")
TAG_V2 = ("[Verse 2: Female Vocal - Soft and Clear, Clean Electric Guitar Arpeggios, Acoustic Guitar, "
          "Warm Piano, Light Pop-Rock Drums]")
TAG_BRIDGE = ("[Bridge: Male Vocal alternating with Female Vocal - Deep Intonation, Emotional Electric Guitar Build, "
              "Powerful Bass, Progressive Live Drums, Rising Cymbals]")
TAG_INTERLUDE = ("[Interlude: Melodic Electric Guitar Solo with Delay, Grand Piano, Electric Bass, "
                 "Powerful Pop-Rock Drums and Warm Cello Lines]")
TAG_FINAL = ("[Final Section: Male & Female Duet - Powerful Emotional Pop-Rock Worship, Full Band Arrangement, "
             "Soft Backing Choir]")
TAG_ENDING = ("[Ending: Very Short Instrumental Outro, max 20s, Brief Final Resolution with Grand Piano and Warm Cello, "
              "No Extended Solo, No Instrumental Repetition, Full Band Decisive Final Chord with Cymbal Resonance, "
              "End Song by 20 seconds]")

# fim de frase: . ? ! (opcionalmente fechando aspas) seguido de espaco e inicio de nova frase
FIM_FRASE = re.compile(r"(?<=[.?!])\s+|(?<=[.?!][”\"])\s+")


def frases(texto):
    return [f.strip() for f in FIM_FRASE.split(texto.strip()) if f.strip()]


def montar(topicos):
    f3 = frases(topicos[2])
    if len(f3) < 2:
        raise ValueError("Topico 3 tem menos de 2 frases; nao da para dividir o Bridge.")
    meio = (len(f3) + 1) // 2          # impar: a voz masculina fica com a frase extra
    t3_m, t3_f = " ".join(f3[:meio]), " ".join(f3[meio:])
    blocos = [
        TAG_INTRO,
        f"{TAG_V1}\n{topicos[0]}",
        f"{TAG_V2}\n{topicos[1]}",
        f"{TAG_BRIDGE}\n\nMale Vocal\n\n{t3_m}\n\nFemale Vocal\n\n{t3_f}",
        TAG_INTERLUDE,
        f"{TAG_FINAL}\n{topicos[3]}",
        TAG_ENDING,
    ]
    return "\n\n".join(blocos)


def palavras(t):
    return re.findall(r"\S+", t)


def conferir(topicos, letra):
    """A letra, sem tags e sem os rotulos Male/Female Vocal, deve ter exatamente as palavras da Saida B."""
    sem_tags = re.sub(r"\[[^\]]*\]", " ", letra)
    sem_tags = re.sub(r"(?m)^(Male|Female) Vocal$", " ", sem_tags)
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

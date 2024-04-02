import os
from split_pattern import split_colors
from motifs_color import generate_motif_colors, get_color_tab


NOM_MOTIF = "monceau"


def mkdir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def main():
    mkdir("output")
    mkdir("output/" + NOM_MOTIF)

    # Sépare les couleurs du pattern pour récupérer les différents motifs
    pattern_path = f"patterns/{NOM_MOTIF}.png"    
    pattern_output_dir =  f"output/{NOM_MOTIF}/motifs"
    mkdir(pattern_output_dir)

    split_colors(pattern_path, pattern_output_dir)
    print("Motifs séparés")

    # Récupère les motifs générés
    colors = get_color_tab("correspondance.csv")
    motifs = os.listdir(pattern_output_dir)

    for motif in motifs:
        num_motif = motif.split(".")[0]
        motif_path = f"{pattern_output_dir}/{motif}"
        motifs_output_dir = f"output/{NOM_MOTIF}/{num_motif}"
        mkdir(motifs_output_dir)        

        generate_motif_colors(motif_path, motifs_output_dir, colors)
        print(f"{num_motif} : OK")


if __name__ == '__main__':
    main()
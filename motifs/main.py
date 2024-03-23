import os
import cv2
from split_pattern import split_colors
from motifs_color import generate_motif_colors, get_color_tab


NOM_MOTIF = "agathe"


def mkdir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def main():
    mkdir("output")
    mkdir("output/" + NOM_MOTIF)

    # Sépare les couleurs du pattern pour récupérer les différents motifs
    pattern_path = f"patterns/{NOM_MOTIF}/pattern.png"
    pattern = cv2.imread(pattern_path, cv2.IMREAD_UNCHANGED)
    
    pattern_output_dir =  f"output/{NOM_MOTIF}/motifs"
    mkdir(pattern_output_dir)

    split_colors(pattern, pattern_output_dir)

    # Récupère les motifs générés
    colors = get_color_tab("correspondance.csv")
    motifs = os.listdir(pattern_output_dir)

    for motif in motifs:
        num_motif = motif.split(".")[0]
        motif_path = f"{pattern_output_dir}/{motif}"
        motifs_output_dir = f"output/{NOM_MOTIF}/{num_motif}"
        mkdir(motifs_output_dir)        

        generate_motif_colors(motif_path, motifs_output_dir, colors)


if __name__ == '__main__':
    main()
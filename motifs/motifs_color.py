import os 
import cv2

NOM_MOTIF = "agathe"


def hex_to_rgb(hex_code:str) -> tuple[int]:
    """ Convertit une couleur hexa en RGB
    In:
        - hex_code (str) : couleur en hexa
    Out:
        - (tuple[int]) : couleur en RGB (R:int, G:int, B:int)
    """
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_bgr(r, g, b):
    return (b, g, r)


def get_color_tab(csv_path:str) -> dict:
    """ Récupère le tableau de correspondance nom_couleur:hexa
    In: 
        - csv_path (str) : chemin vers le csv
    Out:
        - (dict) : dictionnaire associant un code hexa au nom de la couleur
    """
    colors = {}
    with open(csv_path, 'r', encoding="utf-8") as f:
        f.readline()
        for row in f.readlines():
            color, hexa = row.split(";")
            colors[hexa.strip("\n")] = color
    return colors


@DeprecationWarning
def get_colors() -> list[str]:
    """ Récupère la liste des couleurs depuis le fichier colors.txt
    In:
        /
    Out:
        - colors (list[str]) : liste des couleurs en hexa
    """
    colors = []
    with open("colors.txt", "r") as f:
        for color in f.readlines():
            color = color.strip("\n")
            if len(color) == 7:
                colors.append(color)
    return colors


def generate_motif_colors(img_path:str, output_dir:str, colors:dict) -> None:
    """ Génère le motif décliné sous toutes les couleurs de la liste
    In:
        - img_path (str) : chemin vers le motif
        - output_dir (str) : chemin vers le dossier où va se générer les déclinaisons de couleur
        - colors (dict) : dictionnaire hexa:nom_de_la_couleur
    Out:
        /
    """
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    for hexa in colors:
        image[image[:, :, 3] > 50] = list(rgb_to_bgr(*hex_to_rgb(hexa))) + [255]
        output_path = f"{output_dir}/{colors[hexa]}.png"

        cv2.imwrite(output_path, image)


def main():
    motifs = os.listdir("patterns/" + NOM_MOTIF)
    motifs.remove("pattern.png")
    
    colors = get_color_tab("correspondance.csv")

    for motif in motifs:
        img_path = f"patterns/{NOM_MOTIF}/{motif}"
        output_dir = f"motifs/output/{NOM_MOTIF}"
        generate_motif_colors(img_path, output_dir, colors)


if __name__ == '__main__':
    main()
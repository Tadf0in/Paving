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
    return [b, g, r]


def get_color_tab() -> dict:
    """ Récupère le tableau de correspondance nom_couleur:hexa
    In: 
        /
    Out:
        - (dict) : dictionnaire associant un code hexa au nom de la couleur
    """
    colors = {}
    with open("motifs/correspondance.csv", 'r', encoding="utf-8") as f:
        f.readline()
        for row in f.readlines():
            color, hexa = row.split(";")
            colors[hexa.strip("\n")] = color
    return colors


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


def get_motifs(nom:str) -> list[str]:
    """ Retourne la liste des motifs
    In :
        - nom (str) : nom du motif (ex: agathe) 
    Out:
        - (list[str]) : liste des fichiers des motifs
    """
    motifs = os.listdir("patterns/" + nom)
    motifs.remove("pattern.png")
    return motifs


def generate_motif(img_path:str, output_dir:str, colors:list[str], correspondance:dict, num_motif:int) -> None:
    """ Génère le motif décliné sous toutes les couleurs de la liste
    In:
        - img_path (str) : chemin vers le motif
        - output_dir (str) : chemin vers le dossier où va se générer les déclinaisons de couleur
        - colors (list[str]) : liste des couleurs à générer
        - correspondance : tableau de conversion nom:hexa
        - num_motif (int) : numéro du motif
    Out:
        /
    """
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    print(f"{output_dir}/Motif {num_motif}")

    if not os.path.exists(f"{output_dir}/Motif {num_motif}"):
        os.makedirs(f"{output_dir}/Motif {num_motif}")

    for color in colors:
        image[image[:, :, 3] > 50] = rgb_to_bgr(*hex_to_rgb(color)) + [255]
        output_path = f"{output_dir}/Motif {num_motif}/{correspondance[color]}.png"

        cv2.imwrite(output_path, image)


def main():
    colors = get_colors()
    motifs = get_motifs(NOM_MOTIF)
    correspondance = get_color_tab()

    for motif in motifs:
        num_motif = motif.split(".")[0]
        img_path = f"patterns/{NOM_MOTIF}/{motif}"
        output_dir = f"motifs/output/{NOM_MOTIF}"
        generate_motif(img_path, output_dir, colors, correspondance, num_motif)


if __name__ == '__main__':
    main()
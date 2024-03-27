import os 
import cv2
import numpy as np

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


def group_by_4(image:object, joint_size:int=None) -> object:
    """ Regroupe l'image par 4 avant de l'enregistrer
    In:
        - image (cv2.Image) : image a regrouper
        - joint_size (int) : épaisseur du joint
    Out:
        - grouped (cv2.Image) : l'image en quadruple
    """
    size = image.shape[0]

    if joint_size is None:
        joint_size = int(size/100)
    marge = int(joint_size/4)

    output_image = np.zeros((size*2 + joint_size, size*2 + joint_size, 4), dtype=np.uint8)

    # Tourne 3 fois l'image de 90°
    top_right = image
    bottom_right = cv2.rotate(top_right, cv2.ROTATE_90_CLOCKWISE)
    bottom_left = cv2.rotate(bottom_right, cv2.ROTATE_90_CLOCKWISE)
    top_left = cv2.rotate(bottom_left, cv2.ROTATE_90_CLOCKWISE)

    horizontal_joint = np.ones((joint_size+marge*2, size*2+joint_size, 4), dtype=np.uint8) * 255
    vertical_joint = np.ones((size*2+joint_size, joint_size+marge*2, 4), dtype=np.uint8) * 255

    output_image[0:size, 0:size] = top_left
    output_image[size+joint_size:size*2+joint_size, 0:size] = bottom_left
    output_image[0:size, size+joint_size:size*2+joint_size] = top_right
    output_image[size+joint_size:size*2+joint_size, size+joint_size:size*2+joint_size] = bottom_right

    # Joints
    output_image[size-marge:size+joint_size+marge, :] = horizontal_joint
    output_image[:, size-marge:size+joint_size+marge] = vertical_joint

    return output_image


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
        print(output_path)

        resized = cv2.resize(image, (122, 122))

        # joint_size = int(image.shape[0]/100)
        joint_size = 2
        by_4 = group_by_4(resized, joint_size)
        by_16 = group_by_4(by_4, joint_size)

        out_img = cv2.resize(by_16, (480, 493))

        cv2.imwrite(output_path, out_img)


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
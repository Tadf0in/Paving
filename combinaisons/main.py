import cv2
import os
import shutil
import numpy as np
from random import randint


# Nom du pattern + du dossier de sortie qui va se générer
NOM_MOTIF = "agathe" 

# Nombre de combinaisons à générer
NB_A_GENERE = 5

BACKGROUND_COLOR = "#FFFFFF" # couleur en hexa ou "TRANSPARENT"
# Couleurs fixées (dans l'ordre de agathe_colors.txt)
FIXED_COLORS = [
    #"#FF0000",
   # "#FF0000",
    #"#FF0000"
]


def mkdir(name:str) -> None:
    """ Créer le dossier si il n'existe pas déjà
    In:
        - name (str) : nom du dossier
    """
    if not os.path.exists(name):
        os.makedirs(name)


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


def get_colors(txt_file_path:str) -> list[str]:
    """ Récupère la liste des couleurs du pattern depuis le fichier txt
    In:
        - txt_file_path (str) : fichier listant les couleurs
    Out:
        - colors (list[str]) : liste des couleurs en hexa
    """
    colors = []
    with open(txt_file_path, "r") as f:
        for color in f.readlines():
            color = color.strip("\n").strip("\t")
            if len(color) == 7:
                colors.append(color)
    return colors


def get_combinaisons(colors:list[str], nb_colors:int) -> list[str]:
    """ Retourne une combinaisons aléatoire de n couleurs parmis la liste colors
    In:
        - colors (list[str]) : liste des couleurs disponibles en hexa
        - nb_colors (int) : tailel de la liste de sortie
    Out:
        - out (list[str]) : liste de couleurs aléatoires
    """
    out = []
    out += FIXED_COLORS
    for _ in range(nb_colors - len(FIXED_COLORS)):
        out.append(colors[randint(0, len(colors)-1)])
    return out


def group_by_4(image:object) -> object:
    """ Regroupe l'image par 4 avant de l'enregistrer
    In:
        - image (cv2.Image) : image a regrouper
    Out:
        - grouped (cv2.Image) : l'image en quadruple
    """
    size = image.shape[0]

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



def replace_colors(image:object, old_colors:list[str], new_colors:list[str]) -> None:
    """ Remplace les anciennes couleurs du pattern par les nouvelles
    In:
        - image (cv2.Image) : image à traiter (pattern)
        - old_colors (list[str]) : liste des couleurs présentes sur le pattern
        - new_colors (list[str]) : liste des nouvelles couleurs à remplacer
    Out:
        None
    """
    pixels = np.copy(image)
    
    out_name = ""
    for i, color in enumerate(old_colors):
        bgr = rgb_to_bgr(*hex_to_rgb(color))
        mask = np.all(np.abs(image[:, :3] - bgr) == 0, axis=1)
        pixels[mask] = list(rgb_to_bgr(*hex_to_rgb(new_colors[i]))) + [255]
        out_name += new_colors[i] + ","

    if BACKGROUND_COLOR == "TRANSPARENT":
        pixels[pixels[:, 3] != 255] = [0,0,0,0]
    else:
        pixels[pixels[:, 3] != 255] = list(rgb_to_bgr(*hex_to_rgb(BACKGROUND_COLOR))) + [255]

    size = int(np.sqrt(pixels.shape[0]))
    pixels = pixels.reshape(size, size, 4)

    grouped = group_by_4(pixels)
    cv2.imwrite(f"output/{NOM_MOTIF}/{out_name[:-1]}.png", grouped)


def main():
    img_path = f"patterns/{NOM_MOTIF}.png"
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    height, width, channels = image.shape
    size = min(height, width)
    if channels == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image = image[:size, :size, :]
    image = image.reshape(size**2, 4)

    pattern_colors = get_colors(f"patterns/{NOM_MOTIF}_colors.txt")
    colors = get_colors("colors.txt")

    for i in range(1, NB_A_GENERE+1):
        combinaison = get_combinaisons(colors, len(pattern_colors))
        print(i, combinaison)
        replace_colors(image, pattern_colors, combinaison)


if __name__ == '__main__':
    mkdir("output")
    shutil.rmtree(f"output/{NOM_MOTIF}")
    mkdir(f"output/{NOM_MOTIF}")
    main()

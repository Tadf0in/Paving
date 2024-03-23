import cv2
import numpy as np

NOM_MOTIF = "agathe"

colors = [
    "#00BF62",
    "#5E17EA",
    "#938589",
    "#95A288",
    "#9FAED2",
    "#AABDB6",
    "#D7982F",
    "#FF0000",
    "#FFDF5A",
]


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


def split_colors(image, output_dir):
    """ Sépare l'image couleur par couleur
    """
    root_pixels = image.reshape(-1, 4)
    for i, color in enumerate(colors):
        pixels = np.copy(root_pixels)
        bgr = rgb_to_bgr(*hex_to_rgb(color))
        mask = np.all(np.abs(pixels[:, :3] - bgr) == 0, axis=1)
        pixels[~mask] = [0, 0, 0, 0]

        size = int(np.sqrt(pixels.shape[0]))
        out_img = pixels.reshape(size, size, 4)
        
        cv2.imwrite(f"{output_dir}/Motif {i+1}.png", out_img)


def main():
    img_path = f"patterns/{NOM_MOTIF}/pattern.png"
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    split_colors(image)


if __name__ == '__main__':
    main()

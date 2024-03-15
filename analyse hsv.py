import cv2
from sklearn.cluster import KMeans
import numpy as np
import colorsys

image_path = "image.jpg"
colors = ["#024836", "#f2e689", "#15ae86", "#aa39e8", "#cd5d86", "#eb248b", "#ca2589"]

def generate_combinaisons(num_colors=6):
    image = cv2.imread(image_path) # BGR$

    # Convertir l'image lissée en espace de couleurs HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    pixels, shape = get_pixels(hsv_image)

    clusters = get_top_colors(pixels, num_colors)

    generate(pixels, shape, clusters, colors)


def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsv(rgb_color):
    # Convertir les valeurs RGB en valeurs HSV
    hsv_color = colorsys.rgb_to_hsv(rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0)
    # Normaliser les valeurs de teinte et les convertir en degrés
    return (round(hsv_color[0] * 179.0), round(hsv_color[1] * 255.0), round(hsv_color[2] * 255.0))


def hsv_to_rgb(hsv_color):
    # Convertir les valeurs HSV en valeurs RGB
    rgb_color = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(hsv_color[0] / 179.0, hsv_color[1] / 255.0, hsv_color[2] / 255.0))
    return rgb_color


def hsv_to_hex(hsv_color):
    return rgb_to_hex(hsv_to_rgb(hsv_color))

def hex_to_hsv(hex_color):
    return rgb_to_hsv(hex_to_rgb(hex_color))


def get_pixels(image):
    image_array = np.array(image) # transforme l'image en tableau numpy 
    shape = image_array.shape # dimensions de l'image : largeur, longueur, canaux
    pixels = image_array.reshape(-1, shape[2]) # matrice n par 3 (4 si png) : n pixels rgb(a)
    return pixels, shape


def hsv_mask(pixels, target_hsv, tolerance):
    # Gérer la teinte (H) de manière cyclique en degrés
    hue_diff = np.abs(pixels[:, 0] - target_hsv[0])
    hue_diff = np.minimum(hue_diff, 179 - hue_diff)
    
    # Comparer la différence angulaire de la teinte avec la tolérance en degrés
    hue_mask = hue_diff <= tolerance[0]
    
    print(pixels.shape, pixels[:, 1:].shape, target_hsv[1:])

    # Comparer la différence de saturation (S) et de valeur (V) avec la tolérance
    sat_val_diff = np.abs(pixels[:, 1:] - target_hsv[1:])
    sat_val_mask = np.all(sat_val_diff <= tolerance[1:], axis=1)
    
    # Combiner les masques pour former le masque final
    mask = hue_mask & sat_val_mask
    
    return mask


def get_top_colors(pixels, num_colors):
    # Déterminer les couleurs dominantes dans l'espace HSV
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    clusters = np.round(kmeans.cluster_centers_)

    # Trie par ordre décroissant
    clusters_area = {}
    for color in clusters:
        mask = hsv_mask(pixels, color, [10, 100, 100])
        clusters_area[tuple(color)] = pixels[mask].size
    sorted_clusters = sorted(clusters_area.items(), key=lambda x: x[1], reverse=True)

    return [color for color, _ in sorted_clusters]


def generate(pixels, shape, clusters, colors):
    # Remplacer chaque cluster par les couleurs choisies
    for i, color in enumerate(clusters):
        # mask = np.all(np.abs(pixels - hex_to_hsv(color)) <= tolerance, axis=1)
        mask = hsv_mask(pixels, color, [10, 100, 100])
        print(hsv_to_hex(color), pixels[mask].size)
        pixels[mask] = hex_to_hsv(colors[i])

    # Retransforme le tableau numpy en image
    pixels = pixels.reshape(*shape)

    # Convertir de HSV à BGR pour utiliser cv2.imwrite
    image_bgr = cv2.cvtColor(pixels, cv2.COLOR_HSV2BGR)
    smooth = cv2.GaussianBlur(image_bgr, (11, 11), 0)

    # Enregistrer l'image générée avec cv2.imwrite()
    cv2.imwrite("testhsv.jpeg", smooth)


    
img = generate_combinaisons()
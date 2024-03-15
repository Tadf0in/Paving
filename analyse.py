import cv2
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

image_path = "image.jpg"
colors = ["#ff0000", "#00ff00", "0000ff", "#00ffff", "#ff00ff", "ffff00", "0f0f0f"]

def generate_combinaisons(num_colors=7):
    
    print("image : ", image_path)
    image = cv2.imread(image_path)
    pixels, shape = get_pixels(image)

    clusters = get_top_colors(pixels, num_colors)

    generate(pixels, shape, clusters, colors)


def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]


def get_pixels(image):
    image_array = np.array(image) # transforme l'image en tableau numpy 
    shape = image_array.shape # dimensions de l'image : largeur, longueur, canaux
    pixels = image_array.reshape(-1, shape[2]) # matrice n par 3 (4 si png) : n pixels rgb(a)
    return pixels, shape


def get_top_colors(pixels, num_colors, tolerance=5):
    # Détermine les couleurs dominantes
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    clusters = kmeans.cluster_centers_.astype(int)

    # Trie par ordre décroissant
    clusters_area = {}
    for color in clusters:
        mask = np.all(np.abs(pixels - color) <= tolerance, axis=1)
        clusters_area[rgb_to_hex(color)] = pixels[mask].size
    sorted_clusters = [hex_to_rgb(color) for color, _ in sorted(clusters_area.items(), key=lambda x: x[1], reverse=True)]

    print(sorted_clusters, clusters_area)

    return sorted_clusters


def generate(pixels, shape, clusters, colors, tolerance=5):
    # Remplace chaque cluster par les couleurs choisies
    for i, color in enumerate(clusters):
        mask = np.all(np.abs(pixels - color) <= tolerance, axis=1)
        print(color, "->", colors[i], pixels[mask].size)
        pixels[mask] = hex_to_rgb(colors[i])

    # Retransforme le tableau numpy en image
    pixels = pixels.reshape(*shape)
    image_bgr = cv2.cvtColor(pixels, cv2.COLOR_RGB2BGR)
    cv2.imwrite("testcv2.jpeg", image_bgr) 
    
img = generate_combinaisons()
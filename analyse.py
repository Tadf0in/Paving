from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

image_path = "C:/Users/louis/Documents/Fiverr/annaninanina/patterns/agathe python.jpeg"
colors = ["#ff0000", "#00ff00", "0000ff", "#00ffff"]


def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]


def get_top_colors(image, num_colors):
    image_array = np.array(image)

    width = image_array.shape[0]

    # matrice n par 3 (n pixels rgb)
    pixels = image_array.reshape(-1, 3)

    # Détermine les couleurs dominantes
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)
    clusters = kmeans.cluster_centers_.astype(int)

    # Trie par ordre décroissant
    clusters_area = {}
    for i, color in enumerate(clusters):
        mask = np.all(np.abs(pixels - color) <= 10, axis=1)
        clusters_area[rgb_to_hex(color)] = pixels[mask].size

    sorted_clusters = [hex_to_rgb(color) for color, _ in sorted(clusters_area.items(), key=lambda x: x[1], reverse=True)]

    # Replace each cluster with the chosen colors
    for i, color in enumerate(sorted_clusters):
        mask = np.all(np.abs(pixels - color) <= 30, axis=1)
        print(color, "->", colors[i], pixels[mask].size)
        pixels[mask] = hex_to_rgb(colors[i])

    pixels = pixels.reshape((width, width, 3))

    # Convert the modified NumPy array back to an image
    new_image = Image.fromarray(pixels)
    
    return new_image

img = get_top_colors(Image.open(image_path), 4)
img.save("test.jpeg", "JPEG")
import cv2
import numpy as np
from sklearn.cluster import KMeans

def replace_dominant_colors(image_path, output_path, replacement_colors, threshold=50):
    # Charger l'image
    image = cv2.imread(image_path)

    # Convertir l'image en espace de couleurs HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Identifier les couleurs dominantes
    dominant_colors = identify_dominant_colors(hsv_image)

    # Remplacer les couleurs dominantes par les couleurs de remplacement
    for color in dominant_colors:
        for replacement_color in replacement_colors:
            # Calculer la distance euclidienne entre les couleurs dans l'espace HSV
            distance = np.linalg.norm(color - replacement_color)
            if distance < threshold:
                continue  # Ne pas remplacer par une couleur similaire
            # Créer un masque pour les pixels de couleur dominante
            mask = np.all(np.abs(hsv_image - color) < threshold, axis=-1)
            # Remplacer la couleur dominante par la couleur de remplacement
            hsv_image[mask] = replacement_color

    # Convertir l'image de retour en espace de couleurs BGR
    output_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Enregistrer l'image résultante
    cv2.imwrite(output_path, output_image)




def identify_dominant_colors(image, num_colors=7):
    # Convertir l'image en une matrice de pixels
    pixels = image.reshape(-1, 3)

    # Appliquer l'algorithme de clustering K-means
    kmeans = KMeans(n_clusters=num_colors, init='k-means++')
    kmeans.fit(pixels)

    # Récupérer les centres des clusters, qui représentent les couleurs dominantes
    dominant_colors = kmeans.cluster_centers_.astype(int)

    return dominant_colors

# Utilisation de la fonction
image_path = "image.jpg"
output_path = "output_image.jpg"
replacement_colors = [
    (255, 0, 0),  # Rouge
    (0, 255, 0),  # Vert
    (0, 0, 255),   # Bleu
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (127, 127, 127)
]
replace_dominant_colors(image_path, output_path, replacement_colors)

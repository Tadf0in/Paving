import tkinter as tk
from sklearn.cluster import KMeans
import numpy as np
import cv2
import colorsys


class App():
    def __init__(self, root, image_importer, color_picker):
        self.root = root
        self.root.title("annaninanina")

        self.ii = image_importer
        self.cp = color_picker 
        
        self.num_colors = tk.StringVar(self.root)
        self.num_colors_entry = tk.Entry(self.root, textvariable=self.num_colors)
        self.num_colors_entry.pack()

        self.generate_btn = tk.Button(self.root, text="Générer", command=self.generate_combinaisons)
        self.generate_btn.pack(pady=10)


    def generate_combinaisons(self):
        try:
            num_colors = int(self.num_colors.get())
        except ValueError:
            return
        
        image = cv2.imread(self.ii.img_path) # BGR$

        # Convertir l'image lissée en espace de couleurs HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        pixels, shape = self.get_pixels(hsv_image)

        clusters = self.get_top_colors(pixels, num_colors)

        self.generate(pixels, shape, clusters, self.cp.colors)


    def rgb_to_hex(self, rgb_color):
        return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

    def hex_to_rgb(self, hex_code):
        hex_code = hex_code.lstrip('#')
        return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]
    
    def rgb_to_hsv(self, rgb_color):
        # Convertir les valeurs RGB en valeurs HSV
        hsv_color = colorsys.rgb_to_hsv(rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0)
        # Normaliser les valeurs de teinte et les convertir en degrés
        return (round(hsv_color[0] * 179.0), round(hsv_color[1] * 255.0), round(hsv_color[2] * 255.0))

    def hsv_to_rgb(self, hsv_color):
        # Convertir les valeurs HSV en valeurs RGB
        rgb_color = tuple(round(c * 255) for c in colorsys.hsv_to_rgb(hsv_color[0] / 179.0, hsv_color[1] / 255.0, hsv_color[2] / 255.0))
        return rgb_color
        
    def hsv_to_hex(self, hsv_color):
        return self.rgb_to_hex(self.hsv_to_rgb(hsv_color))

    def hex_to_hsv(self, hex_color):
        return self.rgb_to_hsv(self.hex_to_rgb(hex_color))


    def get_pixels(self, image):
        image_array = np.array(image) # transforme l'image en tableau numpy 
        shape = image_array.shape # dimensions de l'image : largeur, longueur, canaux
        pixels = image_array.reshape(-1, shape[2]) # matrice n par 3 (4 si png) : n pixels rgb(a)
        return pixels, shape
    

    def hsv_mask(self, pixels, target_hsv, tolerance):
        # Gérer la teinte (H) de manière cyclique en degrés
        hue_diff = np.abs(pixels[:, 0] - target_hsv[0])
        hue_diff = np.minimum(hue_diff, 360 - hue_diff)
        
        # Comparer la différence angulaire de la teinte avec la tolérance en degrés
        hue_mask = hue_diff <= tolerance[0]
        
        # Comparer la différence de saturation (S) et de valeur (V) avec la tolérance
        sat_val_diff = np.abs(pixels[:, 1:] - target_hsv[1:])
        sat_val_mask = np.all(sat_val_diff <= tolerance[1:], axis=1)
        
        # Combiner les masques pour former le masque final
        mask = hue_mask & sat_val_mask
        
        return mask

    
    def get_top_colors(self, pixels, num_colors):
        # Déterminer les couleurs dominantes dans l'espace HSV
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(pixels)
        clusters = np.round(kmeans.cluster_centers_)

        # Trie par ordre décroissant
        clusters_area = {}
        for color in clusters:
            mask = self.hsv_mask(pixels, color, [10, 100, 100])
            clusters_area[tuple(color)] = pixels[mask].size
        sorted_clusters = sorted(clusters_area.items(), key=lambda x: x[1], reverse=True)

        return [color for color, _ in sorted_clusters]
    

    def generate(self, pixels, shape, clusters, colors):
        # Remplacer chaque cluster par les couleurs choisies
        for i, color in enumerate(clusters):
            # mask = np.all(np.abs(pixels - hex_to_hsv(color)) <= tolerance, axis=1)
            mask = self.hsv_mask(pixels, color, [10, 100, 100])
            print(self.hsv_to_hex(color), pixels[mask].size)
            pixels[mask] = self.hex_to_hsv(colors[i])

            # Retransforme le tableau numpy en image
            pixels = pixels.reshape(*shape)

            # Convertir de HSV à BGR pour utiliser cv2.imwrite
            image_bgr = cv2.cvtColor(pixels, cv2.COLOR_HSV2BGR)
            smooth = cv2.GaussianBlur(image_bgr, (11, 11), 0)

            # Enregistrer l'image générée avec cv2.imwrite()
            cv2.imwrite("testhsv.jpeg", smooth)
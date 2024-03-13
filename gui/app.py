import tkinter as tk
from sklearn.cluster import KMeans
import numpy as np


class App():
    def __init__(self, root, image_path, colors):
        self.root = root
        self.root.title("annaninanina")

        self.image_path = image_path
        self.colors = colors
        
        self.num_colors_entry = tk.Entry(self.root)
        self.num_colors_entry.pack()

        self.generate_btn = tk.Button(self.root, text="Générer", command=self.generate_combinaisons)
        self.generate_btn.pack(pady=10)

        
    def generate_combinaisons(self):
        print("Colors selected:", self.colors)


    def rgb_to_hex(self, rgb_color):
        return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


    def get_top_colors(self, image, num_colors):
        image_array = np.array(image)

        # matrice n par 3 (n pixels rgb)
        pixels = image_array.reshape(-1, 3)

        # Détermine les couleurs dominantes
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(pixels)
        print(kmeans)
        top_colors = kmeans.cluster_centers_.astype(int)

        # Convertit en hexa
        hex_colors = [self.rgb_to_hex(color) for color in top_colors]

        return hex_colors 
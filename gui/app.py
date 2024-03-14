import tkinter as tk
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image


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
        
        print("image : ", self.ii.img_path)
        image = Image.open(self.ii.img_path)
        pixels, shape = self.get_pixels(image)

        clusters = self.get_top_colors(pixels, num_colors)

        generated_img = self.generate(pixels, shape, clusters, self.cp.colors)
        generated_img.save("testgui.png")


    def rgb_to_hex(self, rgb_color):
        return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


    def hex_to_rgb(self, hex_code):
        hex_code = hex_code.lstrip('#')
        return [int(hex_code[i:i+2], 16) for i in (0, 2, 4)]


    def get_pixels(self, image):
        image_array = np.array(image) # transforme l'image en tableau numpy 
        shape = image_array.shape # dimensions de l'image : largeur, longueur, canaux
        pixels = image_array.reshape(-1, shape[2]) # matrice n par 3 (4 si png) : n pixels rgb(a)
        return pixels, shape


    def get_top_colors(self, pixels, num_colors):
        # Détermine les couleurs dominantes
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(pixels)
        clusters = kmeans.cluster_centers_.astype(int)

        # Trie par ordre décroissant
        clusters_area = {}
        for color in clusters:
            mask = np.all(np.abs(pixels - color) <= 100, axis=1)
            clusters_area[self.rgb_to_hex(color)] = pixels[mask].size
        sorted_clusters = [self.hex_to_rgb(color) for color, _ in sorted(clusters_area.items(), key=lambda x: x[1], reverse=True)]

        return sorted_clusters
    

    def generate(self, pixels, shape, clusters, colors):
        # Remplace chaque cluster par les couleurs choisies
        for i, color in enumerate(clusters):
            mask = np.all(np.abs(pixels - color) <= 30, axis=1)
            print(color, "->", colors[i], pixels[mask].size)
            pixels[mask] = self.hex_to_rgb(colors[i])

        # Retransforme le tableau numpy en image
        pixels = pixels.reshape(*shape)
        new_image = Image.fromarray(pixels) 
        
        return new_image
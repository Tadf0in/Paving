import tkinter as tk

class App():
    def __init__(self, root, image_path, colors):
        self.root = root
        self.root.title("annaninanina")

        self.colors = []
        
        self.generate_btn = tk.Button(self.root, text="Générer", command=self.generate_combinaisons)
        self.generate_btn.pack(pady=10)

        
    def generate_combinaisons(self):
        # Placeholder for combination generation
        print("Colors selected:", self.colors)
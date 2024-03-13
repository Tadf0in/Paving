import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImportImage():
    def __init__(self, root):
        self.root = root

        self.img_path = ""

        self.import_btn = tk.Button(self.root, text="Import Image", command=self.import_image)
        self.import_btn.pack(pady=10)

        self.img_label = tk.Label(self.root, width=40, height=20, bg="white")
        self.img_label.pack(pady=10)


    @property
    def img_path(self):
        return self._img_path
    
    @img_path.setter
    def img_path(self, new_path):
        self._img_path = new_path


    # Import une image 
    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])  # Ask the user to select an image file
        if file_path:
            self.img_path = file_path
            self.update_image()


    # Actualise l'interface pour afficher l'image importée
    def update_image(self):
        if self.img_path:
            image = Image.open(self.img_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.img_label.configure(image=photo)
            self.img_label.image = photo 
            self.img_label.config(width=300)
            self.img_label.config(height=300)
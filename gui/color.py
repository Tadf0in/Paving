import tkinter as tk
from tkinter import colorchooser


class ColorPicker:
    def __init__(self, root):
        self.root = root

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.add_btn = tk.Button(self.btn_frame, text="Ajouter", command=self.add_color)
        self.add_btn.pack(side=tk.LEFT, padx=10)

        self.remove_btn = tk.Button(self.btn_frame, text="Supprimer", command=self.remove_color)
        self.remove_btn.pack(side=tk.LEFT, padx=10)

        self.colors_lb = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.colors_lb.pack(pady=10)

        self.colors = []
        self.read_colors_txt()


    @property
    def colors(self):
        return self._colors
    
    @colors.setter
    def colors(self, color_list):
        self._colors = color_list


    # Ajoute une couleur dans la liste
    def add_color(self, hex=None):
        if hex is None:
            try:
                color = colorchooser.askcolor()
            except:
                return
            
            if color[1] is not None:
                hex = color[1]

        if hex not in self.colors:
            self.colors.append(hex)
            self.update_colors_lb()


    # Supprime les couleurs séléctionnées de la liste
    def remove_color(self):
        indexs = self.colors_lb.curselection()
        for index in reversed(indexs):
            del self.colors[index]
        self.update_colors_lb()


    # Actualise l'interface avec la liste actuelle de couleurs
    def update_colors_lb(self):
        self.colors_lb.delete(0, tk.END)

        for color in self.colors:            
            self.colors_lb.insert(tk.END, color)
            self.colors_lb.itemconfig(tk.END, {'bg': color}) 
        
        self.write_colors_txt()

    # Lis les couleurs depuis le fichier colors.txt
    def read_colors_txt(self):
        with open("colors.txt", "r") as f:
            for color in f.readlines():
                hex = color.strip("\n")
                if hex not in self.colors:
                    self.colors.append(hex)
        self.update_colors_lb()
    
    # Enregistre les couleurs dans le fichier colors.txt
    def write_colors_txt(self):
        with open("colors.txt", "w") as f:
            for color in self.colors:
                f.write(color + "\n")


if __name__ == '__main__':
    root = tk.Tk()
    cp = ColorPicker(root)
    root.mainloop()
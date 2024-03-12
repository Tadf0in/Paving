import tkinter as tk
from tkinter import colorchooser

class ColorPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("annaninanina")
        
        self.colors = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.add_btn = tk.Button(self.frame, text="Ajouter", command=self.add_color)
        self.add_btn.pack(side=tk.LEFT, padx=10)

        self.remove_btn = tk.Button(self.frame, text="Supprimer", command=self.remove_color)
        self.remove_btn.pack(side=tk.LEFT, padx=10)

        self.colors_lb = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.colors_lb.pack(pady=10)

        self.generate_btn = tk.Button(self.root, text="Générer", command=self.generate_combinaisons)
        self.generate_btn.pack(pady=10)

    def add_color(self):
        color = colorchooser.askcolor()
        rgb, hex = color
        if color and hex not in self.colors:
            self.colors.append(hex)
            self.update_colors_lb()

    def remove_color(self):
        indexs = self.colors_lb.curselection()
        for index in reversed(indexs):
            del self.colors[index]
        self.update_colors_lb()

    def update_colors_lb(self):
        self.colors_lb.delete(0, tk.END)

        for color in self.colors:
            preview = tk.Label(self.colors_lb, bg=color, width=2)
            preview.grid(row=self.colors.index(color), column=0)
            hexa = tk.Label(self.colors_lb, text=color)
            hexa.grid(row=self.colors.index(color), column=1)

    def generate_combinaisons(self):
        # Placeholder for combination generation
        print("Colors selected:", self.colors)


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPicker(root)
    root.mainloop()

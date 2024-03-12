import tkinter as tk
from tkinter import colorchooser

class ColorPicker:
    def __init__(self, root):
        self.root = root
        
        self.colors = []

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.add_btn = tk.Button(self.btn_frame, text="Ajouter", command=self.add_color)
        self.add_btn.pack(side=tk.LEFT, padx=10)

        self.remove_btn = tk.Button(self.btn_frame, text="Supprimer", command=self.remove_color)
        self.remove_btn.pack(side=tk.LEFT, padx=10)

        self.colors_lb = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.colors_lb.pack(pady=10)

    def get_colors(self):
        return self.colors

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
            self.colors_lb.insert(tk.END, color)
            self.colors_lb.itemconfig(tk.END, {'bg': color})  
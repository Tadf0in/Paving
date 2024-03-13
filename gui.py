import tkinter as tk
from gui.app import App
from gui.color import ColorPicker
from gui.image import ImportImage

if __name__ == "__main__":
    root = tk.Tk()

    ii = ImportImage(root)
    img = ii.img_path

    cp = ColorPicker(root)
    colors = cp.colors

    app = App(root, img, colors)
    
    root.mainloop()

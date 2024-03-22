import tkinter as tk
from gui.app import App
from gui.color import ColorPicker
from gui.image import ImportImage

if __name__ == "__main__":
    root = tk.Tk()

    ii = ImportImage(root)
    cp = ColorPicker(root)

    app = App(root, ii, cp)
    
    root.mainloop()

    app.check_stop()

from PIL import Image
import numpy as np

pixels = np.array(Image.open("C:/Users/louis/Pictures/test.png"))

Image.fromarray(pixels).save("test.png")

# from PIL import Image
# import numpy as np

# # Ouvrir l'image
# input_image = Image.open("C:/Users/louis/Pictures/test.png")

# # Convertir l'image en tableau NumPy
# image_array = np.array(input_image)

# # Afficher les dimensions de l'image et du tableau NumPy
# print("Dimensions de l'image :", input_image.size)
# print("Dimensions du tableau NumPy :", image_array.shape)

# # Sauvegarder l'image à partir du tableau NumPy
# output_image = Image.fromarray(image_array)
# output_image.save("output_image.png")

print("Image sauvegardée avec succès !")
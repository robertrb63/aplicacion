# pip intall Pillow
from PIL import Image
import os


def batch_resize(folder_in, folder_out, width, height):
    for filename in os.listdir(folder_in):
        if filename.endswith(('.png','.jpg','.jped')):
            img = Image.open(os.path.join(folder_in, filename))
            img = img.resize((width, height))
            img.save(os.path.join(folder_out, f"rezised_{filename}"))
            print(f'Archivo {filename} redimensionado a {width}x{height}')
if __name__ == '__main__':
    batch_resize('images', 'images_resized', 800, 600)


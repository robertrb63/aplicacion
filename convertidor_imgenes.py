import os
from PIL import Image

def convertir_imagen(ruta_entrada, formato_salida):
    try:
        nombre_base = os.path.splitext(ruta_entrada)[0]

        with Image.open(ruta_entrada)as img:
            if img.mode in ('RGBA', 'LA') and formato_salida.upper() == 'JPEG':
                img.convert('RGB')

            ruta_salida = f"{nombre_base}.{formato_salida.lower()}"
            img.save(ruta_salida, formato_salida.upper())
            print(f"Imagen convertida correctamente a {formato_salida}")
    except Exception as e:
        print(f"Error al convertir la imagen: {str(e)}")

#imagen = "archivos/Imagenes/Cristiano.PNG"
#print(convertir_imagen(imagen, formato_salida="gif"))
# pip install pyinstaller
import os
import hashlib
import flet as ft  # Ensure the Flet library is installed: pip install flet

def hash_file(filename):
    h = hashlib.md5()
    with open(filename, "rb") as file:
        while chunk := file.read(8096):
            h.update(chunk)
    return h.hexdigest()

def find_duplicates(folder):
    hashes = {}
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            file_hash = hash_file(full_path)
            if file_hash in hashes:
                print(f"Duplicate found: {full_path} = {hashes[file_hash]}")
                delete= input(f" Quieres borrar{full_path}").strip().lower()
                if delete == "si":
                    os.remove(full_path)
                    print(f"Archivo {full_path} borrado.")
                else:
                    print(f"Archivo {full_path}  NO borrado.")  
            else:
                hashes[file_hash] = full_path                                      
            #print(f"Duplicate found: {file_hash}")

        #print(filenames) #aqui imprime el listado de los archivos de la carpeta
#find_duplicates("C:\\Users\Robert\\Pictures\\AI_craciones")
find_duplicates("archios")         
""" 
archivo ="archivos\crea imagenes (1).png"
hash = hash_file(archivo)
hash2 = hash_file("archivos\crea imagenes.png")
print(f"Hash del archivo: {hash}")
print(f"Hash del archivo: {hash2}")
"""
# menu lateral

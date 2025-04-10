import os

def cambiar_nombre(directorio, opcion, valor):
    for nombre_archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, nombre_archivo)   # c://archivos/nombre
        if os.path.isfile(ruta_archivo): 
            nuevo_nombre = ""
            if opcion == "cambiar":
                nuevo_nombre = nombre_archivo.replace(valor[0], valor[1])
            elif opcion == "prefijo":
                nuevo_nombre = f"{valor[0]}_{nombre_archivo}" if isinstance(valor, list) else f"{valor}_{nombre_archivo}"
            else:
                print("Opción no válida. Usa 'cambiar' or 'prefijo'.")
                return

            nueva_ruta = os.path.join(directorio, nuevo_nombre)
            os.rename(ruta_archivo, nueva_ruta)
            print(f"El nombre del archivo {nombre_archivo} ha sido cambiado a {nuevo_nombre}")

ruta = "C:\\Users\\Robert\\Desktop\\archivos"

# cambiar_nombre(ruta, "cambiar", ["Archivo_", ""])
# cambiar_nombre(ruta, "prefijo", ["2024036_", ""])
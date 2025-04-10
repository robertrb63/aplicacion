import os
# pip install PyPDF2
from PyPDF2 import PdfMerger
from pathlib import Path


def fusionar_pdfs(carpeta_entrada, archivo_salidas='pdfs_fusionados.pdf'):
    try:
        #crear Merger
        merger = PdfMerger()
        # verificar si existe la carpeta
        if not os.path.exists(carpeta_entrada):
            print(f'Carpeta {carpeta_entrada} no encontrada')
            return
        # obtener los archivos pdf

        pdfs = [f for f in sorted(Path(carpeta_entrada).glob("*.pdf"))]
        if not pdfs:
            print(f'No se encontraron archivos PDF en la carpeta {carpeta_entrada}')
            return
        print(f"Encontrados {len(pdfs)} archivos pdf")
        # Agregar cada odf al merger
        for pdf in pdfs:
            print(f"Agregando: {pdf.name}")
            merger.append(str(pdf))
        # Guardar el pdf fusionado
        merger.write(archivo_salidas)
        merger.close()
        print(f"\nPDF fusionados correctamente en {archivo_salidas}")

    except Exception as e:
        print(f"Error durante la fusion: {str(e)}")

if __name__ == "__main__":
    carpeta_entrada = "C:\\Users\\Robert\\Desktop\\pdf"
    fusionar_pdfs(carpeta_entrada)


import os
import shutil
def organize_folder(folder):
    file_types = {
        'Imagenes':['.png', '.jpg','jpeg', '.avi', '.gif','.ico'],
        'Videos':['.mp4', '.mov', '.mkv', '.avi', '.wmv'],
        'Documentos':['.txt', '.doc', '.docx', '.pdf', '.xlsx', '.pptx'],
        'Comprimidos':['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Aplicaciones':['.exe', '.msi', '.dll', '.dll'],
        'Otros':['.*','.hex'],
        'Datasets':['.xlsx', '.xls', '.csv','.sav', '.json']
        }
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    print(f'Archivo {filename} movido a  {folder_name}')

#organize_folder('C:\\Users\\Robert\\Documents')             
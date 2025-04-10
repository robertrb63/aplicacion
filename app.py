
import flet as ft
import os
from borrar_duplicados import find_duplicates, delete_file
from organizar_archivos import organize_folder
from redimensinar_imagenes import batch_resize
from convertidor_imgenes import convertir_imagen
from extraer_audio import extraer_audio
from fusionar_pdf import fusionar_pdfs
from cambiar_nombre import cambiar_nombre
"""
en el terminal:
pip install pyinstaller
python -m PyInstaller --onefile app.py
"""
def main(page: ft.Page):
    # Create your app here
    page.title = "Automatizacion de Tareas"
    page.subtitle = "This is a Navigation Rail component"
    # Add your components here
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK
    
    # Tema Personalizado
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_200,
            secondary=ft.Colors.ORANGE,
            background=ft.Colors.GREY_900,
            surface=ft.Colors.GREY_800,
        )
    )

    def change_View(e):
        state["current_view"] = "duplicates"
        selected = e.control.selected_index
        if selected == 0:
            content_area.content = duplicate_files_view
        elif selected == 1:
            state["current_view"] = "organize"
            content_area.content = organize_files_view
        elif selected == 2:
            state["current_view"] = "resize"
            content_area.content = resize_image_view
        elif selected == 3:
            state["current_view"] = "convert"
            content_area.content = convert_images_view
        elif selected == 4:
            state["current_view"] = "audio"
            content_area.content = audio_extraction_view    
        elif selected == 5:
            state["current_view"] = "merge_pdfs"
            content_area.content = merge_pdfs_view 
        elif selected == 6:
            state["current_view"] = "rename"
            content_area.content = rename_riles_view
        content_area.update()

    #Variables de estado
    state = {
        "current_duplicates":[],
        "current_view":"duplicates",
        "resize_input_folder": "",
        "resize_output_folder": "",
        "selecting_resize_output": False,
        "convert_input_file": "",
        "audio_imput_folder":"",
        "audio_extraction_progres":0,
        "total_videos":0,
        "current_video": "",
        "pdf_input_folder":"",
        "rename_input_folder":"",
        "rename_option":"",
        "rename_value": "",
    }
    selected_dir_text = ft.Text(
        "No se ha seleccionado ningun directorio",
        size=16,
        color=ft.Colors.YELLOW_900,
    )

    result_text = ft.Text(size=14, width=ft.FontWeight.BOLD)
    duplicates_list = ft.ListView(
        expand=1,
        spacing=10,
        height=200,
    )

    delete_all_button = ft.ElevatedButton(
        "Eliminar todos los archivos",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_900,
        icon=ft.Icons.DELETE_SWEEP,
        visible=False,
        on_click=lambda e: delete_all_duplicates()
    )

    #Controles par la vista organizar archivos
    organize_dir_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=16,
        color=ft.Colors.BLUE_200,
    )

    organize_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    #Controles par la vista redimensionar imágenes
    resize_input_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=16,
        color=ft.Colors.BLUE_200,
    )

    resize_output_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=16,
        color=ft.Colors.BLUE_200,
    )
  
    resize_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    width_field = ft.TextField(
        label="Ancho",
        value="800",
        width=100,
        text_align=ft.TextAlign.RIGHT,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    height_field = ft.TextField(
        label="Alto",
        value="600",
        width=100,
        text_align=ft.TextAlign.RIGHT,
        keyboard_type=ft.KeyboardType.NUMBER,
    )


    # Controles para la vista de convertir imagenes
    convert_input_text = ft.Text(
        "No se ha encontrado ninguna imagen",
        size=16,
        color=ft.Colors.YELLOW_900
    )
    convert_result_text = ft.Text(size=14, width=ft.FontWeight.BOLD)
    format_dropdown = ft.Dropdown(
        label="Formato Salida",
        width=200,
        options=[
            ft.dropdown.Option("JPEG"),
            ft.dropdown.Option("PNG"),
            ft.dropdown.Option("BMP"),
            ft.dropdown.Option("GIF"),
            ft.dropdown.Option("WEBP"),
        ],
        value="PNG"
    )
    
    # Controles para la vista de extraer audio
    audio_input_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )

    audio_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)
    audio_progress = ft.ProgressBar(width=400, visible=False)
    current_video_text = ft.Text(size=14, color=ft.Colors.BLUE_200)

    # Controles para la vista de mezclar PDFs
    pdf_input_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )
    pdf_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def merge_pdfs():
        try:
            if not state["pdf_input_folder"]:
                pdf_result_text.value = "Error : Selecciona una carpeta con PDFs"
                pdf_result_text.color = ft.Colors.RED_400
                pdf_result_text.update()
                return
            output_file = os.path.join(state["pdf_input_folder"], "pdfs_fusionados.pdf")
            fusionar_pdfs(state["pdf_input_folder"], output_file)
            pdf_result_text.value = f"PDFs mezclados correctamente en:  {output_file}"
            pdf_result_text.color = ft.Colors.GREEN_400
            current_video_text.update()
        except Exception as e:
            pdf_result_text.value = f"Error durante la mezcla : {str(e)}"
            pdf_result_text.color = ft.Colors.RED_400
            pdf_result_text.update()

    # Controles para la vista de renombrar archivos
    rename_input_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=16,
        color=ft.Colors.BLUE_200,
    )

    def on_rename_option_changed(e):
        is_cambiar = e.control.value == "cambiar"
        rename_search_text.visible = is_cambiar
        rename_replace_text.visible = is_cambiar
        rename_prefix_text.visible = not is_cambiar
        rename_search_text.update()
        rename_replace_text.update()
        rename_prefix_text.update()

    rename_option_dropdown = ft.Dropdown(
        label="Opcion de Renombrado",
        options=[
            ft.dropdown.Option("Cambiar"),
            ft.dropdown.Option("Prefijo"),
        ],
        value="Cambiar",
        width=200,
        on_change=on_rename_option_changed, 
    )
    rename_search_text = ft.TextField(
        label="Palabra a buscar",
        width=200,
        visible=True
    )
    rename_search_text = ft.TextField(
        label="Palabra a buscar",
        width=200,
        visible=True
    )
    rename_replace_text = ft.TextField(
        label="Reemplazar por",
        width=200,
        visible=True
    )
    rename_prefix_text = ft.TextField(
        label="Prefijo a agregar",
        width=200,
        visible=False
    )
    rename_result_text =ft.Text(
        size=14, weight=ft.FontWeight.BOLD
    )

    def extract_audio():
        try:
            if not state["audio_imput_folder"]:
                audio_input_text.value = "Error : Selecciona una carpeta con videos"
                audio_input_text.color = ft.Colors.RED_400
                audio_input_text.update()
                return
            
            input_folder = state['audio_imput_folder']
            output_folder = os.path.join(input_folder, "audios")
            os.makedirs(output_folder, exist_ok=True)

            audio_progress.value = 0
            audio_progress.visible = True
            audio_progress.update()

            def progress_callback(current, total, archivo):
                progress = current / total
                audio_progress.value = progress
                audio_progress.update()
                current_video_text.value = f"Procesando {archivo}: {current}/{total}"
                current_video_text.update()
            extraer_audio(input_folder, output_folder, progress_callback)

            audio_result_text.value = "Audio extraido correctamente"
            audio_result_text.color = ft.Colors.GREEN_400
            current_video_text.value = "Proceso finalizado"

        except Exception as e:
            audio_result_text.value = f"Error durante la extraccion : {str(e)}"
            audio_result_text.color = ft.Colors.RED_400
        finally:
            audio_progress.visible = False
            audio_progress.update()
        audio_result_text.update()
        current_video_text.update()


    def rename_files():
        try:
            if not state["rename_input_folder"]:
                rename_result_text.value = "Error:  Selecciona una carpeta"
                rename_result_text.color = ft.Colors.RED_400
                rename_result_text.update()
                return
            option = rename_option_dropdown.value
            if option == "cambiar":
                if not rename_result_text.value:
                    rename_result_text.value = f"Error: Ingresa la palabra a buscar{str(e)}"
                    rename_result_text.color = ft.Colors.RED_400
                    rename_result_text.update()
                    return
                value = [rename_search_text.value, rename_replace_text.value]
            else:
                if not rename_prefix_text.value:
                    rename_result_text.value = "Error: Ingresa el Prefijo"
                    rename_result_text.color = ft.Colors.RED_400
                    rename_result_text.update()
                    return
                value = rename_prefix_text.value
            cambiar_nombre(state["rename_input_folder"], option, value)
            rename_result_text.value = "Archivos renombrados exitosamente"
            rename_result_text.color = ft.Colors.GREEN_500
            rename_result_text.update()

        except Exception as e:
            rename_result_text.value = f"Error al renombrar: {str(e)}"
            rename_result_text.color = ft.Colors.RED_400
            rename_result_text.update()


    def handle_file_picker(e: ft.FilePickerResultEvent):
       if e.files and  len(e.files) > 0:
           file_path = e.files[0].path
           state["convert_input_file"]= file_path
           convert_input_text.value = f"Imagen seleccionada: {file_path}"
           convert_input_text.update()

    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            if state ["current_view"] == "duplicates":
                selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
                selected_dir_text.update()
                scan_directory(e.path)
            elif state ["current_view"] == "organize":
                organize_dir_text.value = f"Carpeta seleccionada: {e.path}"
                organize_dir_text.update()
                organize_directory(e.path)
            elif state ["current_view"] == "resize":
                if state ["selecting_resize_output"]:
                    state["resize_output_folder"] = e.path
                    resize_output_text.value = f"Carpeta de salida seleccionada: {e.path}"
                    resize_output_text.update()
                else:
                    state["resize_input_folder"] = e.path
                    resize_input_text.value = f"Carpeta de entrada seleccionada: {e.path}"
                    resize_input_text.update()
            elif state["current_view"] == "audio":
                state["audio_input_folder"] = e.path
                audio_input_text.value = f"Carpeta seleccionada: {e.path}"
                audio_input_text.update()
            elif state["current_view"] == "merge_pdfs":
                state["pdf_input_folder"] = e.path
                pdf_input_text.value = f"Carpeta seleccionada: {e.path}"
                pdf_input_text.update()
            elif state["current_view"] == "rename":
                state["rename_input_folder"] = e.path
                rename_input_text.value = f"Carpeta seleccionada: {e.path}"
                rename_input_text.update()

    def select_input_folder():
        state["selecting_resize_output"] = False
        folder_picker.get_directory_path()
    
    def select_output_folder():
        state["selecting_resize_output"] = True
        folder_picker.get_directory_path()

    def convert_image():
        try:
            if not state["convert_input_file"]:
                convert_result_text.value = "Error : Debe seleccionar una imagen de entrada."
                convert_result_text.color = ft.Colors.RED_400
                convert_result_text.update()
                return
            if not format_dropdown.value:
                convert_result_text.value = "Error : Debe seleccionar un formato de salida."
                convert_result_text.color = ft.Colors.RED_400
                convert_result_text.update()
                return
            convertir_imagen(state["convert_input_file"], format_dropdown.value)
            convert_result_text.value = "Imagen convertida exitosamente."
            convert_result_text.color = ft.Colors.GREEN_400
            convert_result_text.update()

        except Exception as e:
            print(e)

    def resize_images():
        try:
            if not state["resize_input_folder"] or not state["resize_output_folder"]:
                resize_result_text.value = "Error : Debe seleccionar carpetas de entrada y salida."
                resize_result_text.color = ft.Colors.RED_400
                resize_result_text.update()
                return
            width = int(width_field.value)
            heigth= int(height_field.value)

            if width <= 0 or heigth <=0:
                resize_result_text.value = "Error : Las dimensiones deben ser numéricas y mayores a cero."
                resize_result_text.color = ft.Colors.RED_400
                resize_result_text.update()
                return
            batch_resize(state["resize_input_folder"], state["resize_output_folder"], width, heigth)
            resize_result_text.value ="imagenes redimensionadas Exitosamente"
            resize_result_text.color = ft.Colors.GREEN_400
            resize_result_text.update()
        except Exception:
            resize_result_text.value = "Error:  Ingresa dimensiones validas."
            resize_result_text.color = ft.Colors.RED_400
            resize_result_text.update()
        except Exception as e:
            result_text.value = f"Error: {str(e)}"
            result_text.color = ft.Colors.RED_400
            result_text.update()
            pass

    def organize_directory(directory):
        try:
            organize_folder(directory)
            organize_result_text.value = "Carpeta organizada correctamente."
            organize_result_text.color = ft.Colors.GREEN_400
        except Exception as e:
            organize_result_text.value = f"Error al organizar la carpeta: {str(e)}"
            organize_result_text.color = ft.Colors.RED_400
        organize_dir_text.update()

    def scan_directory(directory):
        duplicates_list.controls.clear()
        state["current_duplicates"] = find_duplicates(directory)
        if not state["current_duplicates"]:
            result_text.value = "No se encontraron archivos duplicados."
            result_text.color = ft.Colors.GREEN_500
            delete_all_button.visible = False
        else:
            result_text.value = f"Se encontraron {len(state['current_duplicates'])} archivos duplicados."
            result_text.color = ft.Colors.ORANGE_400
            delete_all_button.visible = True

            for dup_file, original in state["current_duplicates"]:
                dup_row = ft.Row([
                    ft.Text(
                        f"Archivo duplicado: {dup_file}\nOriginal: {original}",
                        size=14,
                        color=ft.Colors.YELLOW_900,
                        expand=True
                    ),
                    ft.ElevatedButton(
                        "Eliminar",
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_900,
                        on_click=lambda e, path=dup_file: delete_duplicate(path))
                ])
                duplicates_list.controls.append(dup_row)
        duplicates_list.update()
        result_text.update()  
        delete_all_button.update() 
    
    def delete_duplicate(filepath):
        if delete_file(filepath):
            result_text.value = f"Archivo Eliminado: {filepath}"
            result_text.color = ft.Colors.GREEN_500
            for control in duplicates_list.controls[:]:
                if filepath in control.controls[0].value:
                    duplicates_list.controls.remove(control)
            state["current_duplicates"] = [(dup, orig) for dup, orig in state["current_duplicates"] if dup != filepath]
            if not state["current_duplicates"]:
                delete_all_button.visible = False
        else:
            result_text.value = f"No se pudo eliminar el archivo: {filepath}"
            result_text.color = ft.Colors.RED_500
        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    def delete_all_duplicates():
        delete_count = 0
        failed_count = 0
        for dup_file, _ in state["current_duplicates"][:]:
            if delete_file(dup_file):
                delete_count += 1
            else:
                failed_count += 1
        duplicates_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_button.visible = False

        if failed_count == 0:
            result_text.value = f"Todos los archivos han sido eliminados. {delete_count} archivos eliminados con éxito, {failed_count} archivos no se pudieron eliminar."
            result_text.color = ft.Colors.GREEN_500
        else:
            result_text.value = f"{failed_count} archivos no se pudieron eliminar. {delete_count} archivos eliminados con éxito."
            result_text.color = ft.Colors.ORANGE_400
        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    #Configurar los selectores de archivos
    file_picker = ft.FilePicker(
        on_result=handle_file_picker
    )
    file_picker.file_type = ft.FilePickerFileType.IMAGE
    file_picker.allowed_extensions = ["png","jpg","jpeg","gif","bmp","webp"] 
    #handle_file_picker

    # Configurar el selector de carpetas
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.extend([folder_picker, file_picker])

    # Vista Archivos duplicados
    duplicate_files_view = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Eliminar Archivos Duplicados",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_400
                ),
                ft.Row([
                    ft.ElevatedButton(
                    "Seleccionar Carpeta",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    on_click=lambda _e: folder_picker.get_directory_path(),
                ),
                delete_all_button,
                ]),
                
                ft.Container(
                    content=selected_dir_text,
                    margin=ft.margin.only(top=10, bottom=10),
                ),
                result_text,
                
                ft.Container(
                    content=duplicates_list,
                    border=ft.border.all(2, ft.Colors.BLUE_400),
                    border_radius=10,
                    padding=20,
                    margin=ft.margin.only(top=10, bottom=10),
                    bgcolor=ft.Colors.GREY_800,
                    expand=True,
                ),
            ]),
       padding=30,
       expand=True
    )
    
    # Vista de organizacion de archivos
    organize_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Organizar Archivos por Tipo",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_400
                    
                    ),
                    margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                "Seleccionar Carpeta",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=organize_dir_text,
                margin=ft.margin.only(top=10)
            ),
            organize_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Los archivos serán organizados en las siguientes carpetas",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text("- Imágenes (.jpeg, .jpg, .png, .gif)", size=14),
                    ft.Text("- Videos (.mp4, .mov, .avi)", size=14),
                    ft.Text("- Archivos de texto (.txt,.log)", size=14),
                    ft.Text("- Documentos (.pdf,.doc,.docx)", size=14),
                    ft.Text("- Otros (.zip,.rar,.7z,.exe,.msi,.dll,.iso)", size=14),
                ]),
                border=ft.border.all(2, ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )          
        ]),
        padding=30,
        expand=True
    )

    # vista redimensionar imagenes
    resize_image_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Redimensionar Imágenes",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_400
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                    ft.ElevatedButton(
                        "Seleccionar Carpeta de Entrada",
                        icon=ft.Icons.FOLDER_OPEN,
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_900,
                        on_click=lambda _: select_input_folder()
                    ),
                    ft.ElevatedButton(
                        "Seleccionar Carpeta de Salida",
                        icon=ft.Icons.FOLDER_OPEN,
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_900,
                        on_click=lambda _: select_output_folder()
                    ),
                ]),
                ft.Container(
                    content=ft.Column([
                        resize_input_text,
                        resize_output_text
                    ]),
                    margin=ft.margin.only(top=10, bottom=10)
                ),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Dimensiones de la Imagen",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Row([
                        width_field,
                        ft.Text("Ancho: ", size=20),
                        height_field,
                        ft.Text("Alto: ", size=14),
                    ]),
                ]),
                margin=ft.margin.only(bottom=10)
            ),
            ft.ElevatedButton(
                "Redimensionar Imágenes",
                icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: resize_images()
            ),
            resize_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Informacion",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text("- Se procesarán imagenes"),
                    ft.Text("- La imágenes originales no serán mdificadas", size=14),
                    ft.Text("- La imagenes redimensionadas se guardarán con el prefijo 'rezized_' ", size=14),
                ]),
                border=ft.border.all(2, ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True
    )      

    # Vista Convertir Imagenes
    convert_images_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Convertir Imágenes",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_400
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                "Seleccionar Carpeta de Entrada",
                icon=ft.Icons.IMAGE,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: file_picker.pick_files()
            ),
            ft.Container(
                content=convert_input_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            format_dropdown,
            ft.Container(
                margin=ft.margin.only(top=10),
                content=ft.ElevatedButton(
                    "Convertir Imágenes",
                    icon=ft.Icons.IMAGE,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: convert_image()
                ),       
            ), 
            convert_result_text, 
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Información",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text("- Se seleccionarán todos los archivos de la carpeta", size=14),
                    ft.Text("- Se convertirán las imágenes seleccionadas según el formato seleccionado", size=14),     
                ]),
                border=ft.border.all(2, ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True
    )

    # Vista de extraccion de audio
    audio_extraction_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Extracción de Audio",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_400
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                "Seleccionar Carpeta con Videos",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
                
            ft.Container(
                content=audio_input_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.ElevatedButton(
                "Extraer Audio",
                icon=ft.Icons.AUDIOTRACK,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: extract_audio()
            ),
            current_video_text,
            audio_progress,
            audio_result_text
        ]),
        padding=30,
        expand=True

        )
            
    # Menu superior
    content_area =  ft.Container(
        content = duplicate_files_view,
        expand = True
    )


    # Vista de renombrar archivos
    rename_riles_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Renombrar Archivos",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                "Seleccionar Carpeta",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=selected_dir_text,
                margin=ft.margin.only(top=10, bottom=10),
            ),
            ft.Container(
                content=ft.Column([
                    rename_option_dropdown,
                    rename_search_text,
                    rename_replace_text,
                    rename_prefix_text,
                ]),
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.ElevatedButton(
                "Renombrar Archivos",
                icon=ft.Icons.EDIT,
                color=ft.Colors.BLUE_900,
                on_click=lambda _: rename_files()
            ),
            rename_result_text,
        ]),
        padding=30,
        expand=True
    )


    # Vista de fusion pdf

    merge_pdfs_view =ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
            "Fusionar PDFs",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_400
        ),
        margin=ft.margin.only(bottom=20),
            ),
            ft.ElevatedButton(
                "Seleccionar Carpeta con PDFs",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=pdf_input_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.ElevatedButton(
                "Fusionar PDFs",
                icon=ft.Icons.MERGE_TYPE,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: merge_pdfs()
            ),
            pdf_result_text,
        ]),
        padding=30,
        expand=True
    )

    # Menu lateral
    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DELETE_FOREVER,
                selected_icon=ft.Icons.DELETE_FOREVER,
                label="Duplicados",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER_COPY,
                selected_icon=ft.Icons.FOLDER_COPY,
                label="Organizar",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER_COPY,
                selected_icon=ft.Icons.FOLDER_COPY,
                label="Redimensionar",
            ),
             ft.NavigationRailDestination(
                icon=ft.Icons.TRANSFORM,
                selected_icon=ft.Icons.TRANSFORM,
                label="Convertir",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.AUDIOTRACK,
                selected_icon=ft.Icons.AUDIOTRACK,
                label="Extraer Audio",
            ),
             ft.NavigationRailDestination(
                icon=ft.Icons.MERGE_TYPE,
                selected_icon=ft.Icons.MERGE_TYPE,
                label="Fusionar PDFs",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.EDIT,
                selected_icon=ft.Icons.EDIT,
                label="Renombrar",
            ),
            
        ],
        on_change=change_View,
        bgcolor=ft.Colors.GREY_900,
    )

    page.add(
        ft.Row(
            [
                    rail,
                    ft.VerticalDivider(width=1),
                    content_area,
            ],
            expand=True,
        )
    )
    """
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "This is a Navigation Rail component",
                        color=ft.colors.BLUE_200,
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ElevatedButton(
                        "Boton",
                        icon= ft.icons.PLAY_ARROW
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
    )
    """

if __name__ == "__main__":
    ft.app(target=main)

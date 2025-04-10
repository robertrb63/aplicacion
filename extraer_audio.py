import os
# pip install moviepy
from moviepy import VideoFileClip


def extraer_audio(input_folder, output_folder, progress_callback = None):
        
    os.makedirs(output_folder, exist_ok=True) 

    videos = [f for f in os.listdir(input_folder) if f.lower().endswith(('.wav', '.avi', '.mov', '.mkv'))]
    total_videos = len(videos)
    # Procesar cada archivo en la carpeta de entrada

    for index, filename in enumerate(videos, 1):
        input_path = os.path.join(input_folder, filename)
        # if os.path.isfile(input_path) and filename.lower().endswith(('.mp4', '.avi', '.mov')):
        if os.path.isfile(input_path):
            try:
                print(f"Processing: {filename}")
                # Cargar el archivo de video
                video_clip = VideoFileClip(input_path)
                # Obtener la ruta de salida del audio 
                audio_output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".mp3")
                # Extraer el audio y guardarlo 
                video_clip.audio.write_audiofile(audio_output_path)
                video_clip.close()
                print(f"Audio extracted successfully: {audio_output_path}")

                #llamar al callback de progreso, si esta definido
                if progress_callback:
                    progress_callback(index, total_videos)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Ejecutar este script desde la línea de comandos:
    print("Extracion masiva de audios")
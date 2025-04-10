import os
# pip install moviepy
from moviepy import VideoFileClip

input_folder ="videos"  # de esta carpeta de videos se extrae el audio
output_folder ="audios" # en esta carpeta se guardan los audios exraidos

os.makedirs(output_folder, exist_ok=True) 

for index, filename in enumerate(os.listdir(input_folder)):
        input_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_path) and filename.lower().endswith(('.mp4', '.avi', '.mov')):
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

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                    # Ejecutar este script desde la línea de comandos:
print("Extracion masiva de audios")
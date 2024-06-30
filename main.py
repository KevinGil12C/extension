import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube
from moviepy.editor import AudioFileClip
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Rutas para las carpetas de música y videos
parent_dir = os.path.join(os.path.expanduser('~'), 'Music')
parent_dirV = os.path.join(os.path.expanduser('~'), 'Videos')

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir solicitudes desde la extensión de Chrome

@app.route('/')
def index():
    return 'Servidor de descargas activo'

@app.route('/downloadMP3', methods=['POST'])
def descarga_mp3():
    data = request.json
    url = data.get('url')

    def progress_callback(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        logging.info(f"Progreso de descarga MP3: {percentage:.2f}%")

    try:
        video = YouTube(url, on_progress_callback=progress_callback)
        stream = video.streams.get_audio_only().download(parent_dir)
        audioclip = AudioFileClip(stream)
        audioclip.write_audiofile(audioclip.filename.replace('.mp4', '.mp3'))
        os.remove(audioclip.filename)
        mensaje = "Descargado"
        logging.info("Descarga MP3 completada")
    except Exception as e:
        mensaje = f"Error: {str(e)}"
        logging.error(f"Error en descarga MP3: {mensaje}")

    return jsonify({"message": mensaje})

@app.route('/downloadMP4', methods=['POST'])
def descarga_mp4():
    data = request.json
    url = data.get('url')

    try:
        video = YouTube(url)
        
        # Obtener todos los streams disponibles ordenados por resolución
        streams = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        
        # Elegir el mejor stream disponible (el primero en la lista)
        if streams:
            mejor_stream = streams.first()
            if mejor_stream:
                descarga = mejor_stream.download(parent_dirV)
                mensaje = "Descargado en la mejor calidad posible"
                logging.info(f"Descarga MP4 completada en {mejor_stream.resolution}")
            else:
                mensaje = "No se encontró un stream disponible para descargar"
                logging.warning("No se encontró un stream disponible para la URL proporcionada")
        else:
            mensaje = "No se encontraron streams MP4 disponibles para la URL proporcionada"
            logging.warning("No se encontraron streams MP4 disponibles para la URL proporcionada")
            
    except Exception as e:
        mensaje = f"Error: {str(e)}"
        logging.error(f"Error en descarga MP4: {mensaje}")

    return jsonify({"message": mensaje})
def descarga_mp4():
    data = request.json
    url = data.get('url')

    try:
        video = YouTube(url)
        stream = video.streams.get_highest_resolution()
        
        if stream:
            descarga = stream.download(parent_dirV)
            mensaje = "Descargado"
            logging.info("Descarga MP4 completada en la mejor resolución disponible")
        else:
            mensaje = "No se encontró un stream disponible para descargar"
            logging.warning("No se encontró un stream disponible para la URL proporcionada")
            
    except Exception as e:
        mensaje = f"Error: {str(e)}"
        logging.error(f"Error en descarga MP4: {mensaje}")

    return jsonify({"message": mensaje})


if __name__ == '__main__':
    app.run(debug=True, port=8000)

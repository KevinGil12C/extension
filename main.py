import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube
from moviepy.editor import AudioFileClip
import yt_dlp as youtube_dl
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

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(parent_dirV, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        mensaje = "Descargado"
        logging.info("Descarga MP4 completada")
    except Exception as e:
        mensaje = f"Error: {str(e)}"
        logging.error(f"Error en descarga MP4: {mensaje}")

    return jsonify({"message": mensaje})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import UserIP
import os
import yt_dlp
from urllib.parse import quote
import hashlib  # Importa la librería hashlib
import base64
from moviepy.editor import VideoFileClip

#Agregar mas commits github, agregar proyectos.
#1 o 2 paginas deploy.
#primer juntar los recursos para el proyecto

# Obtiene la carpeta de descargas del usuario
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser('~'), 'Music')

def index(request):
    return render(request, 'inicio.html')

@csrf_exempt
def unique_download_view(request, identifier):  # Cambia 'url' por 'identifier'
    try:
        session_key = f'unique_view_{identifier}'  # Cambia 'url' por 'identifier'
        if not request.session.get(session_key):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOADS_FOLDER, '%(title)s.%(ext)s'),
            }
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            url = request.session.get(identifier)  # Cambia 'url' por 'identifier'
            info = ydl.extract_info(url, download=True)
            user_ip = request.META.get('REMOTE_ADDR', '')
            UserIP.objects.create(ip_address=user_ip)  # Guarda la IP en la base de datos
            request.session[session_key] = True

            # Convertir el archivo webm a mp3
            if info.get('_type') == 'playlist':
                for entry in info['entries']:
                    webm_path = os.path.join(DOWNLOADS_FOLDER,f"{entry['title']}.webm")
                    mp3_path = os.path.join(DOWNLOADS_FOLDER, f"{entry['title']}.mp3")
                    video_clip = VideoFileClip(webm_path)
                    audio_clip = video_clip.audio
                    audio_clip.write_audiofile(mp3_path)
                    audio_clip.close()
                    video_clip.close()
            return redirect('index')  # Redirige a la página de inicio

    except Exception as e:
        if 'Video unavailable' in str(e):
            error_message = "El video no esta disponible en tu pais"
            context = {'error_message': error_message}
            return render(request, 'youtube_convertir.html', context)
        else:
            return HttpResponse(f"Error inesperado: {e}")

    raise Http404("URL no válida o problema de descarga")
@csrf_exempt
def youtube_converter_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            e = "Por favor, ingresa una URL válida."
            return render(request, 'index.html', {'error_url':e})

        # Genera un identificador único para la URL
        identifier_bytes = hashlib.md5(url.encode()).digest()
        encoded_identifier = base64.urlsafe_b64encode(identifier_bytes).decode().rstrip("=")

        # Almacena la URL en una variable de sesión usando el identificador como clave
        request.session[encoded_identifier] = url

        download_link = reverse('unique_download', args=[encoded_identifier])
        context = {'url_param': url, 'download_link': download_link}
        return render(request, 'youtube_converter.html', context)

    return render(request, 'youtube_converter.html', context)

def generate_mp3_view(request):
    return HttpResponse("Solicitud no válida")

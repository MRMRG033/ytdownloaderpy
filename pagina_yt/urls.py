from django.urls import path
from . import views  # Importa las vistas de tu aplicación

urlpatterns = [
    path('', views.index, name='index'),  # Ejemplo de URL, cambia 'index' y 'views.index' según tus necesidades
    path('unique/<str:identifier>/', views.unique_download_view, name="unique_download"),
    path('get_download_status/<str:identifier>/', views.get_download_status, name='get_download_status'),
    path('youtube__converter/', views.youtube_converter_view, name="youtube_converter"),
    path('error/', views.generate_mp3_view),
]
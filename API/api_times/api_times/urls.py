from django.urls import path
from gerar_times.views import gerar_time_api

urlpatterns = [
    path('gerar_time/<int:tamanho>/', gerar_time_api, name='gerar_time_api'),
]

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gerar_times.teamComposition import executar_algoritmo

@csrf_exempt
def gerar_time_api(request, tamanho):
    time, avaliacao = executar_algoritmo(int(tamanho))
    response_data = {
        'time': time,
        'avaliacao': avaliacao
    }
    return JsonResponse(response_data)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gerar_times.teamComposition import gerar_time


@csrf_exempt
def gerar_time_api(request, tamanho):
    time = gerar_time(int(tamanho))
    response_data = {'time': time}
    return JsonResponse(response_data)

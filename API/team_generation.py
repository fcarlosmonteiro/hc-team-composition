import requests
import json

def call_api():
    url = 'http://localhost:8000/gerar_time/'

    tamanho_time = str(input('Digite o tamanho do time a ser gerado: '))
    response = requests.post(url+tamanho_time+"/")

    if response.status_code == 200:
        data = response.json()
        print_table(data,tamanho_time)

    else:
        print('Erro ao gerar time.')

def print_table(dicionario, tamanho_time):
    json_string = json.dumps(dicionario)
    json_dict = json.loads(json_string)

    time_ordenado = sorted(json_dict['time'], key=lambda x: x[1])

    print(f"{'ID':<5} {'Nome':<15} {'Papel':<15} {'Nível':<15} {'Linguagem':<15}")
    for i, membro in enumerate(time_ordenado):
        print(f"{i+1:<5} {membro[0]:<15} {membro[1]:<15} {membro[2]:<15} {membro[3]:<15}")


call_api()

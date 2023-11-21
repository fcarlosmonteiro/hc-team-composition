import random
import pandas as pd
from tabulate import tabulate as tb

path='/Users/fcarlos/Documents/Projetos-Git/hc-team-composition/API/api_times/gerar_times/dados.xlsx'

def gerar_time(tamanho):
    dados = pd.read_excel(path).to_dict(orient='records')

    frontend = [d for d in dados if d['Papel'] == 'Frontend']
    backend = [d for d in dados if d['Papel'] == 'Backend']
    design = [d for d in dados if d['Papel'] == 'Design']
    tester = [d for d in dados if d['Papel'] == 'Tester']
    fullstack = [d for d in dados if d['Papel'] == 'Fullstack']

    time = [random.choice(frontend), random.choice(backend),
            random.choice(design), random.choice(tester),
            random.choice(fullstack)]

    papeis = [frontend, backend, design, tester, fullstack]
    num_juniors = len([m for m in time if m['Nível'] == 'junior'])
    for i in range(tamanho - 5):
        prob_junior = (num_juniors / (i + 5))**2
        if random.random() < prob_junior:
            papel = random.choice([p for p in papeis if any(m['Nível'] == 'junior' for m in p)])
        else:
            papel = random.choice(papeis)
        membro = random.choice([m for m in papel if m not in time])
        time.append(membro)
        num_juniors += 1 if membro['Nível'] == 'junior' else 0

    while len(set([m['Nome'] for m in time])) < tamanho:
        time = [random.choice(frontend), random.choice(backend),
                random.choice(design), random.choice(tester),
                random.choice(fullstack)]
        num_juniors = len([m for m in time if m['Nível'] == 'junior'])
        for i in range(tamanho - 5):
            prob_junior = (num_juniors / (i + 5))**2
            if random.random() < prob_junior:
                papel = random.choice([p for p in papeis if any(m['Nível'] == 'junior' for m in p)])
            else:
                papel = random.choice(papeis)
            membro = random.choice([m for m in papel if m not in time])
            time.append(membro)
            num_juniors += 1 if membro['Nível'] == 'junior' else 0

    return [(m['Nome'], m['Papel'], m['Nível'], m['Linguagem']) for m in time]


def expandir_vizinhanca(time):
    times_expandidos = []
    for i in range(4):
        novo_time = time.copy()

        pessoa_orig = random.choice(novo_time)

        papel = pessoa_orig[1]

        df = pd.read_excel(path)
        candidatos = df[(df["Papel"] == papel) & (df["Nome"] != pessoa_orig[0])].values.tolist()

        if not candidatos:
            times_expandidos.append(novo_time)
            continue

        while True:
            pessoa_nova = random.choice(candidatos)
            if pessoa_nova not in novo_time:
                novo_time[novo_time.index(pessoa_orig)] = pessoa_nova
                times_expandidos.append(novo_time)
                break
    return times_expandidos


def avaliar_balanceamento(times):
    resultados = {}
    for i, time in enumerate(times):
        niveis = {"junior": 0, "pleno": 0, "senior": 0}
        for membro in time:
            nivel = membro[2]
            niveis[nivel] += 1 #Incrementa a contagem do nível correspondente
        
        junior_percent = niveis["junior"] / len(time)
        
        if niveis["junior"] == len(time): # Time com todos juniors
            avaliacao = 1 # Recebe o pior valor possível de avaliação
        elif junior_percent > 0.5: # Time com mais de 50% de juniors
            avaliacao = 0.5 * (10 - abs(niveis["junior"] - niveis["pleno"]) - abs(niveis["junior"] - niveis["senior"]) - abs(niveis["pleno"] - niveis["senior"]))
        else:
            avaliacao = 10 - abs(niveis["junior"] - niveis["pleno"]) - abs(niveis["junior"] - niveis["senior"]) - abs(niveis["pleno"] - niveis["senior"])
            if niveis["pleno"] >= niveis["junior"] and niveis["senior"] >= niveis["junior"]:
                # Time com pelo menos 1 pleno ou senior para cada junior
                avaliacao *= 1.2
            elif niveis["junior"] == niveis["pleno"] + niveis["senior"]:
                # Time com mesma quantidade de juniors e plenos+seniors
                avaliacao *= 1.3
        
        resultados[i] = avaliacao
    return resultados

def selecionar_melhor_time(time_inicial, times_expandidos):
    indice_inicial = avaliar_balanceamento([time_inicial])[0]
    melhor_time = time_inicial
    melhor_indice = indice_inicial

    for time in times_expandidos:
        indice_time = avaliar_balanceamento([time])[0]
        print(f"    Vizinho avaliado: {tb(time, headers=['Nome', 'Área', 'Nível', 'Linguagem'])}")
        print(f"        Valor de avaliação: {indice_time}")
        if indice_time > melhor_indice:
            melhor_time = time
            melhor_indice = indice_time
            print(f"        Nova melhor solução: {tb(melhor_time, headers=['Nome', 'Área', 'Nível', 'Linguagem'])}")
    return melhor_time


def executar_algoritmo(tamanho):
    time_inicial = gerar_time(tamanho)
    melhor_solucao = time_inicial
    melhor_indice = avaliar_balanceamento([melhor_solucao])[0]

    for i in range(1, 1000):
        print(f"Iteração {i}")
        times_expandidos = expandir_vizinhanca(melhor_solucao)
        melhor_time = selecionar_melhor_time(melhor_solucao, times_expandidos)
        novo_indice = avaliar_balanceamento([melhor_time])[0]
        if novo_indice > melhor_indice:
            melhor_solucao = melhor_time
            melhor_indice = novo_indice
            print(f"Melhor solução encontrada: {tb(melhor_solucao, headers=['Nome', 'Área', 'Nível', 'Linguagem'])}")
            print(f"Valor de avaliação da melhor solução: {melhor_indice}")
        else:
            print("Nenhuma melhoria encontrada")

    print(f"Melhor solução global encontrada: {tb(melhor_solucao, headers=['Nome', 'Área', 'Nível', 'Linguagem'])}")
    print(f"Valor de avaliação da melhor solução: {melhor_indice}")
    return melhor_solucao, melhor_indice



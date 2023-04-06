import random
import pandas as pd
from tabulate import tabulate as tb


def gerar_time(tamanho):
    # 1. Ler a planilha de dados e armazenar seus dados em uma lista de dicionários
    dados = pd.read_excel('dados.xlsx').to_dict(orient='records')

    # 2. Separar os dados em listas de cada papel
    frontend = [d for d in dados if d['Papel'] == 'Frontend']
    backend = [d for d in dados if d['Papel'] == 'Backend']
    design = [d for d in dados if d['Papel'] == 'Design']
    tester = [d for d in dados if d['Papel'] == 'Tester']
    fullstack = [d for d in dados if d['Papel'] == 'Fullstack']

    # 3. Selecionar um elemento aleatório de cada lista de papel
    time = [random.choice(frontend), random.choice(backend),
            random.choice(design), random.choice(tester),
            random.choice(fullstack)]

    # 4. Selecionar os demais membros do time aleatoriamente a partir das listas de cada papel
    papeis = [frontend, backend, design, tester, fullstack]
    for i in range(tamanho - 5):
        papel = random.choice(papeis)
        membro = random.choice(papel)
        time.append(membro)

    # 5. Verificar se não há membros repetidos no time
    while len(set([m['Nome'] for m in time])) < tamanho:
        time = [random.choice(frontend), random.choice(backend),
                random.choice(design), random.choice(tester),
                random.choice(fullstack)]
        for i in range(tamanho - 5):
            papel = random.choice(papeis)
            membro = random.choice(papel)
            time.append(membro)

    # 6. Retornar o time com as informações de nome, papel, nível e linguagem
    return [(m['Nome'], m['Papel'], m['Nível'], m['Linguagem']) for m in time]


def expandir_vizinhanca(time):
    times_expandidos = []
    for i in range(4):
        # 1. Criar uma cópia do time original
        novo_time = time.copy()

        # 2. Selecionar aleatoriamente uma pessoa do time
        pessoa_orig = random.choice(novo_time)

        # 3. Obter o papel dessa pessoa
        papel = pessoa_orig[1]

        # 4. Obter a lista de pessoas do mesmo papel que a pessoa selecionada
        df = pd.read_excel("dados.xlsx")
        candidatos = df[(df["Papel"] == papel) & (df["Nome"] != pessoa_orig[0])].values.tolist()

        if not candidatos:
            times_expandidos.append(novo_time)
            continue

        # 5. Selecionar aleatoriamente uma pessoa da lista de mesmo papel que a pessoa selecionada
        pessoa_nova = random.choice(candidatos)

        # 6. Substituir a pessoa selecionada pela pessoa escolhida do mesmo papel
        novo_time[novo_time.index(pessoa_orig)] = pessoa_nova

        # 7. Adicionar o novo time à lista de times expandidos
        times_expandidos.append(novo_time)

    return times_expandidos

def avaliar_balanceamento(times):
    '''
    O valor de diff_abs indica a diferença absoluta entre as contagens de membros de cada par de níveis (junior, pleno e senior)
    em um time. Quanto menor o valor de diff_abs, mais balanceado é o time, pois significa que a diferença entre as contagens
    de membros de cada nível é menor. um valor de diff_abs muito baixo pode não ser necessariamente o melhor para um time, pois pode
    indicar que há pouca diversidade nos níveis de seus membros. Por outro lado, um valor muito alto de diff_abs pode indicar que 
    há uma grande discrepância nas habilidades e experiências dos membros do time, o que também pode ser prejudicial para o 
    desempenho do time.
    '''
    resultados = {}
    for i, time in enumerate(times):
        niveis = {"junior": 0, "pleno": 0, "senior": 0}
        for membro in time:
            nivel = membro[2]
            niveis[nivel] += 1 #Incrementa a contagem do nível correspondente
        
        # Calcula a diferença absoluta entre as contagens de cada par de níveis
        diff_abs = abs(niveis["junior"] - niveis["pleno"]) + abs(niveis["junior"] - niveis["senior"]) + abs(niveis["pleno"] - niveis["senior"])
        resultados[i] = diff_abs
    return resultados

def selecionar_melhor_time(time_inicial, times_expandidos):
    # Calcula o índice de balanceamento do time inicial
    indice_inicial = avaliar_balanceamento([time_inicial])[0]

    # Calcula o índice de balanceamento de cada time expandido
    indices_expandidos = avaliar_balanceamento(times_expandidos)

    # Seleciona o time com o menor índice de balanceamento
    melhor_indice = min(indices_expandidos.values())
    melhor_time = None
    for i, indice in indices_expandidos.items():
        if indice == melhor_indice:
            melhor_time = times_expandidos[i]
            break

    # Retorna o melhor time encontrado
    if melhor_indice < indice_inicial:
        return melhor_time
    else:
        return time_inicial

time_inicial = gerar_time(7)
melhor_time=time_inicial
for i in range(1,100):
    times_expandidos = expandir_vizinhanca(melhor_time)
    melhor_time = selecionar_melhor_time(melhor_time, times_expandidos)

print(tb(melhor_time, headers=['Nome', 'Área', 'Nível', 'Linguagem']))


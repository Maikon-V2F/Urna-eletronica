import pickle
import os
import matplotlib.pyplot as plt

dados_candidatos = []
dados_eleitores = []

# Função para imprimir o menu
def imprimirMenu():
    print(
        " Selecione uma opção: \n 1 - Ler arquivo de candidatos\n 2 - Ler arquivo de eleitores \n 3 - Iniciar votação \n 4 - Apurar votos \n 5 - Mostrar resultados \n 6 - Fechar programa"
    )

# Função para abrir arquivo de dados
def abrirArquivo(arquivo, dados_lista, campos):
    with open(arquivo, "r") as arquivo:
        for linha in arquivo:
            partes = linha.split()
            dados_dict = {}
            for i, campo in enumerate(campos):
                dados_dict[campo] = partes[i]
            dados_lista.append(dados_dict)
            print(dados_dict)  # Mova esta linha para dentro do loop
    print(f"Dados carregados com sucesso.")
    imprimirMenu()
    receberOpcao()

# Função para abrir arquivo dos candidatos
def arquivoCandidatos():
    global dados_candidatos
    campos_candidatos = ["nome", "numero", "partido", "uf", "funcao"]
    dados_candidatos = abrirArquivo("candidatos.txt", dados_candidatos, campos_candidatos)

# Função para abrir arquivo dos eleitores
def arquivoEleitores():
    global dados_eleitores
    campos_eleitores = ["nome", "rg", "titulo", "municipio", "uf"]
    dados_eleitores = abrirArquivo("eleitores.txt", dados_eleitores, campos_eleitores)

def votacao():
    # Verificar se os arquivos de candidatos e eleitores foram carregados anteriormente
    if not dados_candidatos or not dados_eleitores:
        print("Erro: É necessário carregar os arquivos de candidatos e eleitores antes de iniciar a votação.")
        return
    
    uf_urna = input("Informe o estado onde a urna está localizada: ")

    while True:
        titulo_eleitor = input("Informe o número do título de eleitor: ")

        eleitor_encontrado = False
        for eleitor in dados_eleitores:
            if eleitor['titulo'] == titulo_eleitor:
                eleitor_encontrado = True
                print(
                    f"\nEleitor encontrado:\nNome: {eleitor['nome']} {eleitor['rg']}\nEstado: {eleitor['uf']}\n"
                )
                break

        if eleitor['uf'] == uf_urna:
            print("Eleitor é do estado de %s. Pode votar." %(uf_urna))
        else:
            print("Eleitor não é do estado de %s. Não pode votar." %(uf_urna))
            novo_voto = input("\nRegistrar novo voto (S ou N)? ").upper()
            if novo_voto != 'S':
                break
            else:
                continue

        if not eleitor_encontrado:
            print("Eleitor não encontrado. Verifique o número do título de eleitor.")
            novo_voto = input("Registrar novo voto (S ou N)? ").upper()
            if novo_voto != 'S':
                break
            else:
                continue

        votos = {}

        cargos = ["Deputado Federal", "Deputado Estadual", "Deputado Estadual", "Senador", "Governador", "Presidente"]

        for cargo in cargos:
            voto = input(f"Informe o voto para {cargo}: ").upper()

            candidato_encontrado = False
            for candidato in dados_candidatos:
                if candidato['numero'] == voto:
                    candidato_encontrado = True
                    print(
                        f"\nCandidato encontrado:\nNome: {candidato['nome']} | Partido: {candidato['partido']}\n"
                    )
                    confirma = input("Confirma (S ou N)? ").upper()
                    if confirma == 'S':
                        votos[cargo] = f"Candidato {candidato['nome']} | {candidato['partido']}"
                        salvarVoto(votos)  # Salva o voto imediatamente
                    else:
                        print(f"Voto para {cargo} cancelado.")
                    break

            if not candidato_encontrado:
                votos[cargo] = "Voto Nulo"
                salvarVoto(votos)  # Salva o voto imediatamente
                print(f"Candidato não encontrado! Voto Nulo.")

        print("\nVotos registrados:")
        for cargo, voto in votos.items():
            print(f"{cargo}: {voto}")

        novo_voto = input("\nRegistrar novo voto (S ou N)? ").upper()
        if novo_voto != 'S':
            break
        else:
            imprimirMenu()
            receberOpcao()

def salvarVoto(votos):
    with open("votos.pickle", "ab") as arquivo:
        pickle.dump(votos, arquivo)

def apurarVotos():
    total_eleitores = 0
    total_votos_nominais = 0
    total_brancos = 0
    total_nulos = 0
    votos_candidatos = {}

    with open("votos.pickle", "rb") as arquivo:
        while True:
            try:
                votos = pickle.load(arquivo)

                total_eleitores += 1
                total_votos_nominais += 1

                for cargo, voto in votos.items():
                    if voto == "Voto Nulo":
                        total_nulos += 1
                    elif voto == "Voto Branco":
                        total_brancos += 1
                    else:
                        if cargo not in votos_candidatos:
                            votos_candidatos[cargo] = {}

                        if voto not in votos_candidatos[cargo]:
                            votos_candidatos[cargo][voto] = 1
                        else:
                            votos_candidatos[cargo][voto] += 1
            except EOFError:
                break

    return total_eleitores, total_votos_nominais, total_brancos, total_nulos, votos_candidatos

def exibirResultados(total_eleitores, total_votos_nominais, total_brancos, total_nulos, votos_candidatos):
    print("Apuração dos votos:")
    print(f"Eleitores Aptos: {total_eleitores}")
    print(f"Total de Votos Nominais: {total_votos_nominais}")
    print(f"Brancos: {total_brancos}")
    print(f"Nulos: {total_nulos}")

    for cargo, votos_candidato in votos_candidatos.items():
        print(f"\nCandidatos para o cargo {cargo}:")
        for candidato, quantidade in votos_candidato.items():
            porcentagem = (quantidade / total_votos_nominais) * 100
            print(
                f"Candidato: {candidato} | Cargo: {cargo} | Votos: {quantidade} ({porcentagem:.2f}%)"
            )

def gera_grafico(titulo, votos):
    candidatos = list(votos.keys())
    quantidade_votos = list(votos.values())

    plt.bar(candidatos, quantidade_votos, color='blue')
    plt.title(titulo)
    plt.xlabel('Candidatos')
    plt.ylabel('Quantidade de Votos')
    plt.show()

# Função para receber a opção desejada
def receberOpcao():
    opcaoRecebida = int(input("Digite a opção desejada: "))

    if opcaoRecebida == 1:
        arquivoCandidatos()
    elif opcaoRecebida == 2:
        arquivoEleitores()
    elif opcaoRecebida == 3:
        votacao()
    elif opcaoRecebida == 4:
        total_eleitores, total_votos_nominais, total_brancos, total_nulos, votos_candidatos = apurarVotos()
        exibirResultados(total_eleitores, total_votos_nominais, total_brancos, total_nulos, votos_candidatos)
    elif opcaoRecebida == 5:
        # Gera gráfico
        titulo = "Resultado da Eleição"
        votos = {"Candidato 1": 25, "Candidato 2": 30, "Candidato 3": 20, "Candidato 4": 15}
        gera_grafico(titulo, votos)
    elif opcaoRecebida == 6:
        print("Programa encerrado.")
        exit()
    else:
        print("Opção inválida. Tente novamente.")

    imprimirMenu()
    receberOpcao()

# Chamar a função para imprimir o menu
imprimirMenu()

# Chamar a função para receber a opção do usuário
receberOpcao()

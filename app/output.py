import csv

def gerar_csv(dados, nome_arquivo):

    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        # Escreva os dados
        escritor.writerows(dados)

# # Exemplo de uso:
# dados = [
#     {'nome': 'João', 'idade': 30, 'cidade': 'São Paulo'},
#     {'nome': 'Maria', 'idade': 25, 'cidade': 'Rio de Janeiro'},
#     {'nome': 'Pedro', 'idade': 35, 'cidade': 'Brasília'}
# ]

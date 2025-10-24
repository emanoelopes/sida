import pandas as pd
import random
import os

# Lista de nomes comuns no Brasil
nomes = ["João", "Maria", "Pedro", "Ana", "Carlos", "Lúcia", "Marcos", "Clara", "Rafael", "Sandra"]
sobrenomes = ["Silva", "Santos", "Oliveira", "Pereira", "Ferreira", "Rodrigues", "Almeida", "Costa", "Gonçalves", "Lima"]
bairros_fortaleza = ["Aldeota", "Amaralina", "Bom Jardim", "Cajazeiras", "Conquista", "Damas", "Encruzilhada", "Fátima", "Guararapes", "Horizonte"]

# Gerando dados aleatórios com nomes únicos
nomes_unicos = []
nomes_usados = set()

for i in range(500):
    while True:
        nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        if nome not in nomes_usados:
            nomes_usados.add(nome)
            nomes_unicos.append(nome)
            break

dados = {
    'nome_aluno': nomes_unicos,
    'nota_2bim': [round(random.uniform(0, 10), 1) for _ in range(500)],
    'faltas': [random.randint(0, 10) for _ in range(500)],
    'pontuacao': [random.randint(0, 10) for _ in range(500)],
    'regiao': [f"{random.choice(bairros_fortaleza)}" for _ in range(500)],
    'resultado_final': [round(random.uniform(0, 10), 1) for _ in range(500)]
}

# Criando um DataFrame com os dados gerados
df = pd.DataFrame(dados)

# Função para exportar a planilha para Excel
def exportar_planilha(dataframe):
    try:
        # Criando o diretório de saída se não existir
        output_dir = 'data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Exportando para Excel
        output_path = os.path.join(output_dir, 'planilha_exemplo_500.xlsx')
        dataframe.to_excel(output_path, index=False)
        print(f"Planilha exportada com sucesso para: {output_path}")
        return True
        
    except Exception as e:
        print(f"Erro ao exportar planilha: {e}")
        return False

# Função principal
def main():
    print("Gerando dados aleatórios para 500 alunos...")
    print(f"DataFrame criado com {len(df)} registros")
    print(f"Colunas: {list(df.columns)}")
    print("\nPrimeiras 5 linhas:")
    print(df.head())
    
    # Exportando a planilha
    if exportar_planilha(df):
        print("Processo concluído com sucesso!")
    else:
        print("Erro no processo de exportação.")

if __name__ == "__main__":
    main()
import pandas as pd
import random
import os

# Lista expandida de nomes comuns no Brasil
nomes = ["João", "Maria", "Pedro", "Ana", "Carlos", "Lúcia", "Marcos", "Clara", "Rafael", "Sandra",
         "José", "Antônio", "Francisco", "Paulo", "Fernando", "Roberto", "Ricardo", "Eduardo", "Márcio", "Felipe",
         "Lucas", "Gabriel", "Bruno", "Diego", "André", "Thiago", "Rodrigo", "Leandro", "Alexandre", "Daniel",
         "Ana", "Juliana", "Camila", "Patrícia", "Aline", "Sandra", "Fernanda", "Beatriz", "Juliana", "Larissa",
         "Amanda", "Natália", "Vanessa", "Mariana", "Letícia", "Bianca", "Cristina", "Renata", "Simone", "Tatiana"]

# Lista expandida de sobrenomes
sobrenomes = ["Silva", "Santos", "Oliveira", "Pereira", "Ferreira", "Rodrigues", "Almeida", "Costa", "Gonçalves", "Lima",
              "Araújo", "Barbosa", "Cardoso", "Dias", "Fernandes", "Gomes", "Henrique", "Inácio", "Jesus", "Klein",
              "Machado", "Nascimento", "Oliveira", "Pinto", "Queiroz", "Ribeiro", "Souza", "Teixeira", "Vieira", "Xavier",
              "Yamamoto", "Zimmermann", "Andrade", "Brito", "Cavalcanti", "Duarte", "Espinosa", "Freitas", "Guimarães", "Hoffmann"]
bairros_fortaleza = ["Aldeota", "Amaralina", "Bom Jardim", "Cajazeiras", "Conquista", "Damas", "Encruzilhada", "Fátima", "Guararapes", "Horizonte"]

# Gerando dados aleatórios com nomes únicos (abordagem otimizada)
nomes_unicos = []
nomes_usados = set()

# Calcular combinações possíveis
total_combinacoes = len(nomes) * len(sobrenomes)
print(f"Total de combinações possíveis: {total_combinacoes}")

# Se temos combinações suficientes, usar abordagem de unicidade
if total_combinacoes >= 500:
    for i in range(500):
        tentativas = 0
        while tentativas < 50:  # Limite de tentativas
            nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            if nome not in nomes_usados:
                nomes_usados.add(nome)
                nomes_unicos.append(nome)
                break
            tentativas += 1
        
        # Se não conseguiu nome único, usar um nome com identificador
        if tentativas >= 50:
            nome_base = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            nome = f"{nome_base} ({i+1})"
            nomes_unicos.append(nome)
else:
    # Se não temos combinações suficientes, permitir repetições com identificadores
    for i in range(500):
        nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        if nome in nomes_usados:
            nome = f"{nome} ({i+1})"
        nomes_usados.add(nome)
        nomes_unicos.append(nome)

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
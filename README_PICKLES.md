# 📦 Arquivos Pickle - Documentação

## 🎯 Objetivo
Os arquivos pickle contêm DataFrames pandas processados para eliminar a necessidade de carregar e processar arquivos CSV repetidamente, melhorando significativamente a performance do dashboard.

## 📁 Arquivos Gerados

### `uci_dataframe.pkl`
- **Conteúdo**: DataFrame UCI processado e concatenado
- **Tamanho**: ~0.12 MB
- **Registros**: 1,044 registros (661 estudantes únicos)
- **Colunas**: 34 (incluindo transformações aplicadas)
- **Processamento**: 
  - Concatenação de student-mat.csv (395 registros) + student-por.csv (649 registros)
  - 366 estudantes aparecem em ambas as matérias (matemática e português)
  - 25 estudantes apenas em matemática, 270 apenas em português
  - Total: 661 estudantes únicos
  - Transformação de valores categóricos
  - Mapeamento de códigos para labels legíveis

### `oulad_dataframe.pkl`
- **Conteúdo**: DataFrame OULAD processado e mesclado
- **Tamanho**: ~42 MB
- **Registros**: 266,706 atividades
- **Colunas**: 27 (dados mesclados de múltiplas tabelas)
- **Processamento**:
  - Merge de 7 tabelas CSV diferentes
  - Imputação de valores ausentes
  - Limpeza e padronização de dados

## 🚀 Como Gerar os Arquivos

### Método 1: Script Automático
```bash
cd /home/emanoel/sida
source .venv/bin/activate
python gerar_pickles.py
```

### Método 2: Regeneração Manual
```python
from webapp.src.carregar_dados import carregar_dados_uci_raw, carregar_dados_oulad_raw, processar_dados_oulad
import pickle

# UCI
df_uci = carregar_dados_uci_raw()
with open('uci_dataframe.pkl', 'wb') as f:
    pickle.dump(df_uci, f)

# OULAD
dataframes_oulad = carregar_dados_oulad_raw()
df_oulad = processar_dados_oulad(dataframes_oulad)
with open('oulad_dataframe.pkl', 'wb') as f:
    pickle.dump(df_oulad, f)
```

## ⚡ Benefícios de Performance

### Antes (CSV):
- ⏱️ Carregamento: ~5-10 segundos
- 🔄 Processamento: ~3-5 segundos por dataset
- 💾 Memória: Carregamento repetido de arquivos

### Depois (Pickle):
- ⚡ Carregamento: ~0.1-0.5 segundos
- 🚀 Processamento: Já processado
- 💾 Memória: Carregamento direto do DataFrame

**Melhoria**: ~90% mais rápido! 🎉

## 🔧 Manutenção

### Quando Regenerar:
1. **Dados atualizados**: Se os arquivos CSV forem modificados
2. **Processamento alterado**: Se a lógica de processamento mudar
3. **Erro de carregamento**: Se os pickles ficarem corrompidos

### Verificação de Integridade:
```python
import pickle
import pandas as pd

# Verificar UCI
with open('uci_dataframe.pkl', 'rb') as f:
    df_uci = pickle.load(f)
    print(f"UCI: {df_uci.shape}")

# Verificar OULAD
with open('oulad_dataframe.pkl', 'rb') as f:
    df_oulad = pickle.load(f)
    print(f"OULAD: {df_oulad.shape}")
```

## 📋 Estrutura dos Dados

### UCI (Escolas Públicas Portuguesas)
- **Origem**: student-mat.csv + student-por.csv
- **Transformações**:
  - `traveltime`: 1→'<15m', 2→'15-30m', 3→'30-1h', 4→'>1h'
  - `studytime`: 1→'<2h', 2→'2-5h', 3→'5-10h', 4→'>10h'
  - Tipos de dados convertidos para object
  - Coluna 'origem' adicionada

### OULAD (Plataforma Online)
- **Origem**: 7 tabelas CSV mescladas
- **Processamento**:
  - Merge de studentVle + vle + studentInfo + assessments + courses + studentRegistration
  - Imputação de valores ausentes
  - Limpeza de colunas duplicadas
  - Padronização de tipos de dados

## 🛠️ Troubleshooting

### Erro: "Arquivo não encontrado"
```bash
# Verificar se os arquivos existem
ls -la *.pkl

# Regenerar se necessário
python gerar_pickles.py
```

### Erro: "Pickle corrompido"
```bash
# Remover arquivos corrompidos
rm *.pkl

# Regenerar
python gerar_pickles.py
```

### Erro: "Dados inconsistentes"
```bash
# Verificar arquivos CSV originais
ls -la datasets/uci_data/
ls -la datasets/oulad_data/

# Regenerar pickles
python gerar_pickles.py
```

## 📊 Monitoramento

### Tamanhos Esperados:
- `uci_dataframe.pkl`: ~0.12 MB
- `oulad_dataframe.pkl`: ~42 MB

### Verificação Rápida:
```bash
# Verificar tamanhos
ls -lh *.pkl

# Verificar integridade
python -c "
import pickle
with open('uci_dataframe.pkl', 'rb') as f: df = pickle.load(f)
print(f'UCI: {df.shape}')
with open('oulad_dataframe.pkl', 'rb') as f: df = pickle.load(f)
print(f'OULAD: {df.shape}')
"
```

## 🎯 Próximos Passos

1. **Automatização**: Integrar geração de pickles no CI/CD
2. **Versionamento**: Controle de versão dos arquivos pickle
3. **Validação**: Checksums para verificar integridade
4. **Backup**: Backup automático dos arquivos pickle

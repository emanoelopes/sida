# Análise e Otimização do requirements.txt

## 📊 Situação Anterior
- **176 dependências** no requirements.txt original
- Muitas bibliotecas do sistema operacional (Debian/Ubuntu)
- Dependências desnecessárias para o projeto
- Incluía pacotes como: ansible, docker, PyQt, etc.

## 🎯 Dependências Reais do Projeto

### Core Dependencies (Obrigatórias)
- `streamlit` - Framework principal do dashboard
- `pandas` - Manipulação de dados
- `numpy` - Computação numérica
- `matplotlib` - Visualizações básicas
- `seaborn` - Visualizações estatísticas
- `scikit-learn` - Machine Learning
- `scipy` - Estatísticas avançadas

### Dependências Opcionais
- `plotly` - Visualizações interativas (página analisador)
- `missingno` - Análise de dados faltantes (OULAD)
- `pygwalker` - Análise interativa (opcional)
- `tabula-py` - Processamento de PDF (página analisador)

### Dependências de Desenvolvimento
- `pytest` - Testes unitários
- `pathlib2` - Utilitários de caminhos

## ✅ Otimização Implementada

### Antes: 176 dependências
### Depois: 24 dependências (86% de redução!)

### Benefícios:
1. **Instalação mais rápida** - Menos dependências para baixar
2. **Menos conflitos** - Redução de incompatibilidades
3. **Menor footprint** - Projeto mais limpo
4. **Manutenibilidade** - Fácil de entender e atualizar

## 📋 Requirements.txt Otimizado

```txt
# Core dependencies for the educational dashboard project
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
scikit-learn>=1.3.0
scipy>=1.10.0

# Data visualization and analysis
plotly>=5.15.0
missingno>=0.5.0

# Optional interactive analysis
pygwalker>=0.3.0

# PDF processing (for analisador page)
tabula-py>=2.7.0

# Testing
pytest>=7.0.0

# Development and utilities
pathlib2>=2.3.0
```

## 🔍 Verificação de Funcionamento
- ✅ Todas as dependências principais testadas
- ✅ Ambiente virtual funcionando
- ✅ Projeto executando corretamente
- ✅ Backup do requirements.txt original criado

## 📁 Arquivos Criados
- `requirements_otimizado.txt` - Versão limpa
- `requirements_backup.txt` - Backup do original
- `ANALISE_REQUIREMENTS.md` - Esta documentação

## 🚀 Próximos Passos
1. Testar instalação em ambiente limpo
2. Documentar dependências opcionais
3. Considerar versionamento mais específico se necessário

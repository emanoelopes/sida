# Guia de Configuração do SIDA

## Pré-requisitos
- Python 3.9 ou superior
- Git

## Instalação Rápida
```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd sida

# Executar script de setup
chmod +x setup_environment.sh
./setup_environment.sh

# Ativar ambiente virtual
source venv/bin/activate

# Executar aplicação
streamlit run webapp/home_1.py
```

## Estrutura do Projeto
- `webapp/` - Aplicação Streamlit principal
- `datasets/` - Datasets UCI e OULAD
- `data/` - Dados processados
- `app/` - Configurações da aplicação Flask
- `docs/` - Documentação técnica

## Comandos Úteis
- Executar: `streamlit run webapp/home_1.py`
- Testes: `pytest`
- Docker: `docker build -t sida . && docker run -p 8501:8501 sida`
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY . .

# Expor porta do Streamlit
EXPOSE 8501

# Comando para executar
CMD ["streamlit", "run", "webapp/home_1.py", "--server.port=8501", "--server.address=0.0.0.0"]
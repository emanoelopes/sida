FROM python:3.9-slim-buster

WORKDIR /webapp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expor a porta padrão do Streamlit.
EXPOSE 8501

CMD ["streamlit", "run", "home.py"]
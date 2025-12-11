# Clareia: Sistema de Identifcação de Dificuldades de Aprendizagem

Sistema de identificação de dificuldades de aprendzagem por meio de IA.

Produto Educacional Digital para compor os requisistos exigidos pelo Mestrado Profissional em Tecnologia Educacional.

## 🐳 Execução com Docker (Recomendado)

O projeto está totalmente configurado para execução em qualquer dispositivo usando Docker:

```bash
# Execução simples
docker-compose up -d

# Acesse: http://localhost:8501
```

### Comandos Docker Compose:
- `docker-compose up -d` - Executar em background
- `docker-compose down` - Parar serviços
- `docker-compose logs -f` - Ver logs em tempo real
- `docker-compose --profile dev up -d` - Modo desenvolvimento

## 🚀 Execução local (Streamlit)

```bash
pip install -r requirements.txt
streamlit run webapp/home.py
```

## ☁️ Deploy manual no Hugging Face Spaces (Streamlit)

1. Criar um Space no Hugging Face usando SDK **Streamlit**.
2. Definir `App file` como `webapp/home.py`.
3. Confirmar Python pelo `runtime.txt` (`python-3.11`).
4. Setar secrets necessários (ex.: `OPENAI_API_KEY`) em *Settings > Repository secrets* do Space.
5. Fazer upload inicial dos arquivos (via `git push` para o repo do Space ou upload web).
6. Para sincronizar manualmente com o GitHub: após cada `git push` no GitHub, repetir o push para o repositório do Space (ou usar o upload web).


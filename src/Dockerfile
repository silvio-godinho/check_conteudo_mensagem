FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "src/main.py"]

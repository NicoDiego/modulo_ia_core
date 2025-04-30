# 1) Base image
FROM python:3.10-slim

# 2) Imposta la working directory
WORKDIR /app

# 3) Copia requirements e installa dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copia tutto il progetto
COPY . .

# 5) Comando di avvio
ENTRYPOINT ["./start.sh"]
CMD []


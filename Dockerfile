# Stage 2: runtime
FROM python:3.10-slim
WORKDIR /app

# Installa git e build-essential per poter pip install git+...
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    git \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copia e installa le dipendenze
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice nel builder
COPY . .

# Stage 2: runtime
FROM python:3.10-slim

WORKDIR /app

# Installa bash per lo start.sh
RUN apt-get update \
 && apt-get install -y --no-install-recommends bash \
 && rm -rf /var/lib/apt/lists/*

# Crea un utente non-root
RUN useradd -m appuser
USER appuser

# Copia dipendenze e codice dal builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Rendi eseguibile lo script di avvio
RUN chmod +x start.sh

# Monta i volumi per persistere dati
VOLUME ["/app/data", "/app/output", "/app/logs"]

# Entry point
ENTRYPOINT ["./start.sh"]

# -----------------------------------------------------------------------------
# Stage 1: builder – installa git e build tools, e installa tutte le dipendenze
# -----------------------------------------------------------------------------
FROM python:3.10-slim AS builder

WORKDIR /app

# Installa git (per pip install git+…) e build-essential
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git \
      build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copia requirements e installa tutto, incluso il pacchetto git+
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice nel builder
COPY . .

# -----------------------------------------------------------------------------
# Stage 2: runtime – immagine pulita, senza git o build-tools
# -----------------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

# Installa bash per lo start.sh
RUN apt-get update \
 && apt-get install -y --no-install-recommends bash \
 && rm -rf /var/lib/apt/lists/*

# Copia solo ciò che serve dal builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Rendi eseguibile lo script e assicura che root possieda /app
RUN chmod +x /app/start.sh \
 && chown -R root:root /app

# Monta i volumi per persistere dati
VOLUME ["/app/data", "/app/output", "/app/logs"]

# Entry point verso lo script d’avvio (girerà come root)
ENTRYPOINT ["./start.sh"]

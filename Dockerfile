# Stage 1: builder
 FROM python:3.10-slim AS builder

 WORKDIR /app

-# Installa build essentials (se servono)
-RUN apt-get update && apt-get install -y --no-install-recommends \
-    build-essential \
- && rm -rf /var/lib/apt/lists/*

+# Installa git e build essentials per clonare e compilare dipendenze da git
+RUN apt-get update \
+ && apt-get install -y --no-install-recommends \
+    git \
+    build-essential \
+ && rm -rf /var/lib/apt/lists/*

 # Copia e installa le dipendenze
 COPY requirements.txt .
 RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

 # Copia il codice
 COPY . .
 
# Stage 2: runtime
 FROM python:3.10-slim

 WORKDIR /app

 # Installa bash per start.sh
-RUN apt-get update \
- && apt-get install -y --no-install-recommends bash \
- && rm -rf /var/lib/apt/lists/*
+RUN apt-get update \
+ && apt-get install -y --no-install-recommends bash \
+ && rm -rf /var/lib/apt/lists/*

 # Crea utente non-root
 RUN useradd -m appuser
 USER appuser

 # Copia file e dipendenze dal builder
 COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
 COPY --from=builder /usr/local/bin /usr/local/bin
 COPY --from=builder /app /app

 RUN chmod +x start.sh

 EXPOSE 8501
 VOLUME ["/app/data","/app/output","/app/logs"]
 ENTRYPOINT ["./start.sh"]

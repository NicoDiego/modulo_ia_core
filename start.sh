#!/usr/bin/env bash
set -e

# 1) Posizionati nella dir dello script
cd "$(dirname "$0")"

# 2) Se usi venv in locale, attivalo (in container non c’è venv)
if [ -f "venv/bin/activate" ]; then
  echo "[start.sh] Attivo venv locale"
  source venv/bin/activate
else
  echo "[start.sh] Nessun venv, uso Python di sistema"
fi

# 3) Crea le cartelle se non esistono
mkdir -p logs data output

# 4) (Facoltativo) prova a cambiare permessi, ma ignora l’errore su bind-mount Windows
chmod 777 logs || true

# 5) Esegui lo script principale
python run_ai.py "$@"

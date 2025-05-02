#!/usr/bin/env bash
set -e

# Spostati nella dir dello script
cd "$(dirname "$0")"

# Se esiste un venv (solo per l'uso in locale), attivalo
if [ -f "venv/bin/activate" ]; then
  echo "[start.sh] Attivo venv locale"
  source venv/bin/activate
else
  echo "[start.sh] Nessun venv, uso Python di sistema"
fi

# Esegui direttamente lo script principale (le dipendenze sono già nell'immagine)
python run_ai.py "$@"

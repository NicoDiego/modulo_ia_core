#!/usr/bin/env bash
set -e

# 1) Posizionati nella dir dello script
cd "$(dirname "$0")"

# 2) Attiva o crea virtualenv
if [ ! -d "venv" ]; then
  echo "Creazione venv..."
  python3 -m venv venv
fi
source venv/bin/activate

# 3) Installa dipendenze
pip install --upgrade pip
pip install -r requirements.txt

# 4) Avvia pipeline
echo "Avvio pipeline AI..."
python run_ai.py "$@"

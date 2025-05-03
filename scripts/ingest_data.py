# scripts/ingest_data.py

import os
import shutil

input_dir = "data/raw"
output_dir = "data/processed"

os.makedirs(output_dir, exist_ok=True)

# Copia tutti i file da raw a processed
for filename in os.listdir(input_dir):
    src_path = os.path.join(input_dir, filename)
    dst_path = os.path.join(output_dir, filename)
    shutil.copyfile(src_path, dst_path)

print("✅ Ingestione completata: dati copiati da raw a processed.")

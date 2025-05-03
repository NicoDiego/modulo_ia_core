# File: scripts/ingest_data.py

import os
import shutil

def main():
    src_dir  = "data/raw"
    dst_dir  = "data/processed"
    os.makedirs(dst_dir, exist_ok=True)

    # copia tutti i file da raw → processed
    for fname in os.listdir(src_dir):
        src_path = os.path.join(src_dir, fname)
        dst_path = os.path.join(dst_dir, fname)
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src_path} → {dst_path}")

    print("✅ Ingestion completed")

if __name__ == "__main__":
    main()

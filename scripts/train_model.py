# scripts/train_model.py
import argparse
import logging
from modules.trainer import Trainer

def main():
    parser = argparse.ArgumentParser(description="Nightly Model Training")
    parser.add_argument("--data-dir",  default="data/processed",
                        help="Directory dei dati preprocessati")
    parser.add_argument("--out-dir",   default="models",
                        help="Directory dove salvare il modello e le metriche")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s",
        handlers=[
            logging.FileHandler(f"{args.out_dir}/training.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("trainer")

    logger.info(f"Starting training with data in {args.data_dir}")
    trainer = Trainer(data_dir=args.data_dir, model_dir=args.out_dir)
    metrics = trainer.train()
    logger.info(f"Training completed. Metrics: {metrics}")

if __name__ == "__main__":
    main()

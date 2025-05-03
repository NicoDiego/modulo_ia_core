import argparse, logging
from modules.deployer import Deployer

def main():
    parser = argparse.ArgumentParser("Deploy modello")
    parser.add_argument("--model-path", default="models/model.h5",
                        help="Percorso del file modello da deployare")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s")
    deployer = Deployer()
    deployer.deploy(args.model_path)

if __name__ == "__main__":
    main()

# modules/trainer.py
import os

class Trainer:
    def __init__(self, data_dir: str, model_dir: str):
        self.data_dir = data_dir
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

    def train(self):
        """
        Qui inserisci la tua logica di training:
        - carica i dati da self.data_dir
        - definisci e addestra il modello
        - salva i pesi in self.model_dir
        - ritorna un dizionario di metriche
        """
        # --- esempio fittizio ---
        # data = load_my_data(self.data_dir)
        # model = build_my_model()
        # history = model.fit(data)
        # model.save(os.path.join(self.model_dir, "model.h5"))
        # metrics = {"accuracy": history.history["accuracy"][-1]}
        # return metrics
        raise NotImplementedError("Implementa il metodo train()")

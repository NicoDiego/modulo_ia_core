# modules/evaluator.py
import os
import numpy as np
# da voi: import del framework ML (tensorflow, torch, sklearn…)

class Evaluator:
    def __init__(self, model_dir: str, data_dir: str):
        self.model_dir = model_dir
        self.data_dir  = data_dir

    def evaluate(self) -> dict:
        """
        - Carica il modello da self.model_dir (es. model.h5)
        - Carica dati di test da self.data_dir
        - Calcola metriche (accuracy, loss, f1…)
        - Ritorna un dict, es. {"accuracy": 0.92, "f1": 0.88}
        """
        # --- stub di esempio ---
        # model = load_model(os.path.join(self.model_dir, "model.h5"))
        # X_test, y_test = load_test_data(self.data_dir)
        # preds = model.predict(X_test).argmax(axis=1)
        # accuracy = (preds == y_test).mean()
        # return {"accuracy": float(accuracy)}
        raise NotImplementedError("Implementa evaluate()")

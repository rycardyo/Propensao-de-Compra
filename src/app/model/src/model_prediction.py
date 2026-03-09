import joblib 
from pathlib import Path 
import os 

root_path = Path(__file__).resolve().parents[2]

class RankerModel: 
    def __init__(self,
                 model_path = os.path.join(root_path, 'model/resources/model_definition/best_xgboost_model.pkl')): 

        self.model_path = model_path
        self._load_model() 


    def _load_model(self):
        self.model = joblib.load(self.model_path)

        return self.model

    def predict(self, 
                dataset):
        
        return self.model.predict_proba(dataset)[:,1]
import pandas as pd 
from sklearn import joblib 
import os 

class DataPreparation:
    def __init__(self,
                 dataset,
                 encoders_path = './encoders/',
                 model_path = './model_definition/'):
        

        self.expected_columns = ['']
        self.dataset = dataset 
        self.encoders_path = encoders_path
        self.model_path = model_path
        
    
    def _encode_features(self):
        ...
        
    def check_dataset_structure(self):
        
        if self.dataset.columns:
            ...

    def add_features(self):
        self.dataset['faixa_etaria'] = self.dataset.Age.apply(lambda x: 10*(x//10))
        self.dataset['entre_30_50'] = self.dataset.Age.apply(lambda x: 1 if (x>=30) and (x<=50) else 0)

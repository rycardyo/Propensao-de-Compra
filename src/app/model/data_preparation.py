import pandas as pd 
from sklearn import joblib 
import os 
import json 

class DataPreparation:
    def __init__(self,
                 dataset,
                 encoders_path = './encoders/',
                 model_path = './model_definition/',
                 verbose : bool = False):
        
        '''
        dataset: 
            pd.DataFrame with the same structure as the one used for training the model. 
            encoders_path: Folder path where the encoders (scalers and mappings) are stored 
            model_path:    Folder path where the trained model is stored 
            verbose : If True, prints the steps of pipeline 

        
        '''

        self.expected_columns = ['']
        self.dataset = dataset 
        self.encoders_path = encoders_path
        self.model_path = model_path
        self.verbose    = verbose  

    def pipeline(self):
        ''' 
        Returns the dataset with the same structure as the one used for training the model. 
        
        '''
        self._add_features() 
        self._encode_features()

        if self.verbose:
            print('Data preparation pipeline completed.')

        return self.dataset

    def _encode_features(self):
        if self.verbose:
            print('Encoding features...')

        with open(self.encoders_path + '/.config.json', 'r') as f:
            config_encoder = json.load(f)

        scalers = config_encoder['scalers']
        mappings = config_encoder['mappings'] 

        for feature in scalers: 
            scaler = joblib.load(os.path.join(self.encoders_path, scalers[feature]))
            self.dataset[feature] = scaler.transform(self.dataset[feature].values)

        for feature in mappings: 
            with open(os.path.join(self.encoders_path, mappings[feature]), 'r') as f:
                mapping = json.load(f)

            self.dataset[feature] = self.dataset[feature].map(mapping)
        
        return self.dataset


    def check_dataset_structure(self):
        
        if self.dataset.columns:
            ...

    def _add_features(self):
        if self.verbose:
            print('Adding features...')

        self.dataset['faixa_etaria'] = self.dataset.Age.apply(lambda x: 10*(x//10))
        self.dataset['entre_30_50'] = self.dataset.Age.apply(lambda x: 1 if (x>=30) and (x<=50) else 0)

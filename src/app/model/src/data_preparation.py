import pandas as pd 
import joblib 
import os 
import json 
from pathlib import Path 
import numpy  as np

root_path = Path(__file__).resolve().parents[2]


class DataPreparation:
    def __init__(self,
                 dataset,
                 encoders_path = os.path.join(root_path, 'model/resources/encoders/'),
                 model_path = os.path.join(root_path, 'model/resources/model_definition/'),
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
        self._set_inference_columns()
        
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
            try:

                values = np.array(self.dataset[feature].values)
                self.dataset[f'{feature}_encoded'] = scaler.transform(values)
                self.dataset.drop(columns = feature, 
                                  inplace = True)
                
            except:

                values = np.array(self.dataset[feature].values.reshape(-1,1))
                self.dataset[f'{feature}_encoded'] = scaler.transform(values)
                self.dataset.drop(columns = feature, 
                                  inplace = True)
                

        for feature in mappings: 
            with open(os.path.join(self.encoders_path, mappings[feature]), 'r') as f:
                mapping = json.load(f)

            self.dataset[f'{feature}_encoded'] = self.dataset[feature].map(mapping)
            self.dataset.drop(columns = feature, 
                                  inplace = True)
        
        return self.dataset
    
    def _set_inference_columns(self):
        with open(os.path.join(root_path, 'model/resources/dataset/.required_columns.json'), 'r') as f:
            inference_columns = json.load(f)["inference_columns"]

        self.dataset = self.dataset[inference_columns]

    def check_dataset_structure(self):
        
        if self.dataset.columns:
            ...

    def _add_features(self):
        if self.verbose:
            print('Adding features...')

        self.dataset['faixa_etaria'] = self.dataset['age'].apply(lambda x: 10*(x//10))
        self.dataset['entre_30_50'] = self.dataset['age'].apply(lambda x: 1 if (x>=30) and (x<=50) else 0)
        self.dataset.rename(columns = {'gender' : 'sexo_feminino'}, inplace = True)
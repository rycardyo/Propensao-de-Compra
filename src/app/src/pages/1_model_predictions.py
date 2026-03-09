import streamlit as st
import pandas as pd 
import sys 
from pathlib import Path
import os 

root_path = Path(__file__).resolve().parents[2]
sys.path.append(os.path.join(root_path, 'model/src'))
print(root_path)
from model_prediction  import RankerModel
from data_preparation  import DataPreparation


st.title('Model Predictions')

st.markdown(''' 
### Hey there! 
    This is my predictions page 
            
    See you later!
''')

dataset = pd.read_csv(st.query_params['datasetFName'])
data_preparator = DataPreparation(dataset, verbose = True)
dataset_to_model = data_preparator.pipeline()

model = RankerModel()
dataset_to_model['Predictions'] = model.predict(dataset_to_model)

st.dataframe(dataset_to_model.sort_values(by = 'Predictions'), 
             ascending = False)
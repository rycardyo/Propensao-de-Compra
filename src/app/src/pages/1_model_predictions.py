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


st.title('Ranked List')

st.markdown(''' Lista de clientes rankeados por propensão de compra (%)''')


dataset = pd.read_csv(st.query_params['datasetFName']).drop(columns=['Unnamed: 0', 'unnamed: 0','id','response'])
data_preparator = DataPreparation(dataset, verbose = True)
dataset_to_model = data_preparator.pipeline()

model = RankerModel()
propensity_to_buy = model.predict(dataset_to_model)

dataset['Propensity_to_buy'] = propensity_to_buy * 100
dataset['Propensity_to_buy'] = dataset['Propensity_to_buy'].apply(lambda x: round(x,2))
st.dataframe(dataset.sort_values(by = 'Propensity_to_buy', ascending = False))
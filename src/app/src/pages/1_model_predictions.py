import streamlit as st
import pandas as pd 
import sys 
sys.path.append('../../model/src')
from model_prediction  import RankerModel
from data_preparation  import DataPreparation

st.title('Model Predictions')

st.markdown(''' 
### Hey there! 
    This is my predictions page 
            
    See you later!
''')

dataset = pd.read_csv(st.query_params['datasetFName'])
dataset_to_model = DataPreparation()
import streamlit as st
import pandas as pd 


st.title('Model Predictions')

st.markdown(''' 
### Hey there! 
    This is my predictions page 
            
    See you later!
''')

dataset = pd.read_csv(st.query_params['datasetFName'])
params = st.query_params
st.dataframe(dataset.sample(2))
import pandas as pd 


class DataPreparation:
    def __init__(self,
                 dataset):

        self.expected_columns = ['']
        self.dataset = dataset 

    def check_dataset_structure(self):
        
        if self.dataset.columns
    df_3 = pd.read_csv('./data/df_3.csv')
    df_3['faixa_etaria'] = df_3.Age.apply(lambda x: 10*(x//10))
    df_3['entre_30_50'] = df_3.Age.apply(lambda x: 1 if (x>=30) and (x<=50) else 0)
    df_3['Annual_Premium_br'] = df_3.Annual_Premium.apply(lambda x: x * 0.057)

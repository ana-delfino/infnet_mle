"""
This is a boilerplate pipeline 'PreparacaoDados'
generated using Kedro 0.19.12
"""
import pandas as pd
from sklearn.model_selection import train_test_split

def filter_dataset(data: pd.DataFrame):
    data = data[['lat','lon','minutes_remaining','period','playoffs','shot_distance','shot_made_flag']]
    data = data.dropna()
    data['shot_made_flag'] = data['shot_made_flag'].astype(int)
    return data

def split_data(data: pd.DataFrame, test_size, random_state)-> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    X = data.drop('shot_made_flag', axis=1)  
    y = data['shot_made_flag'] 

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    y_train = y_train.to_frame(name='shot_made_flag')
    y_test = y_test.to_frame(name='shot_made_flag')

    return X_train, X_test, y_train, y_test

def dataset_metrics(X_train, X_test, test_size):
    metrics = {
        'train_df_size': X_train.shape[0],
        'test_df_size': X_test.shape[0],
        'test_size_perc': test_size
    }

    return {
        key: {'value': float(value) if isinstance(value, (int, float)) else value, 'step': 1}
        for key, value in metrics.items()
    }
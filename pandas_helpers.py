import numpy as np
import pandas as pd

def apply_preprocess_steps(features_preprocess_steps, df):
    print(10*"=", 'Preprocess Features')
    for step in features_preprocess_steps:
        print('step', step)    
        if step['type'] == 'one_hot_encode':
            df, _ = auto_one_hot_encoder(df, step['column'], step['params'])
    return df

def gui_create_preprocess_step(df):
    step = {}
    step['type'] = input('type? [ one_hot_encode | scale ]: ')
    
    if step['type'] == 'one_hot_encode':
        while True:
            print('Columns:', df.columns)
            step['column'] = input('Choose Column: ')
            if step['column'] in df.columns:
                break
        
        df, step['params'] = auto_one_hot_encoder(df, step['column'])
        
    return df, step
        
    


def auto_one_hot_encoder(df, col, params={}):
    """
    Create a one hot encoding automatically or based on 'params'.
    
    Ex.
        d1 = {'col1': ['q', 'w', 'e'], 'col2': ['p', 'p', 'p']}
        df1 = pd.DataFrame(data=d1)
        d2 = {'col1': ['w', 'a', 'z'], 'col2': ['p', 'p', 'p']}
        df2 = pd.DataFrame(data=d2)
        df, params = auto_one_hot_encoder(df1, 'col1')
        df, params = auto_one_hot_encoder(df2, 'col1')

    TODO:
        Add column for N/A and option to remove those rows
    """
    if 'categories' not in params.keys():
        params['categories'] = df[col].unique().tolist()
    if 'default' not in params.keys():
        params['default'] = col + '_' + params['categories'][0]
    
    
    for val in params['categories']:
        df[col +'_' + val] = np.where(df[col] == val, 1, 0)
    
    df[col + '_others'] = np.where(df[col].isin(params['categories']) != True, 1, 0)
    # Remove originial
    df = df.drop(col, axis=1)
    # Remove default
    df = df.drop(params['default'], axis=1)
    return df, params



    
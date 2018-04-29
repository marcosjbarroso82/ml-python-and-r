import numpy as np
import pandas as pd

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

    """
    if 'categories' not in params.keys():
        params['categories'] = df[col].values
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


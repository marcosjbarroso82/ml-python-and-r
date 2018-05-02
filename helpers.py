import json, os
from gui_helpers import gui_get_column, gui_get_file_path
from pandas_helpers import apply_preprocess_steps, gui_create_preprocess_step
import pandas as pd
from sklearn.cross_validation import train_test_split


class SessionManager:
    
    conf = {}
    
    def __init__(self, name, conf_file=None, df_path=None, *args, **kwargs):
        if conf_file:
            self.load_session_from_file(conf_file)
        self.name = name
        
        if df_path:
            assert os.path.isfile(df_path), 'Dataset file Not Found!'
            self.conf['df_path'] = df_path
            
        self.conf['random_state'] = '0' # TODO: Move to sanitize
    
    def sanitize(self):
        """
        Use this function to set all the required states and not having to checkit all the time
        TODO: Implement
        """
        pass
    
    def gui_start(self):
        print('gui_start')
        if 'df_path' not in self.conf.keys():
            self.conf['df_path'] = gui_get_file_path('Enter Dataset file path')
        
        df = self.get_dataset()
        
        if 'target_column' not in self.conf.keys():
            self.conf['target_column'] = gui_get_column(df, 'Enter the Target column')
            
        if 'test_size' not in self.conf.keys(): # TODO: Move to sanitize
            # TODO: Ask user for right rate
            self.conf['test_size'] = '0.3'
        
        if not 'steps' in self.conf.keys():
            self.conf['steps'] = []
        
    def apply_preprocess_steps(self, df):
        return apply_preprocess_steps(self.conf['steps'], df)
    
    def gui_create_preprocess_steps(self, df):
        print('Create Preprocess Step')
        while True:
            if input('Do you wish to create an extra preprocess step [y/N]: ') != 'y':
                break
            
            df, step_params = gui_create_preprocess_step(df)
            self.conf['steps'].append(step_params)
        return df       
        
    def separate_feature_from_target(self, df):
        X = df.drop(self.conf['target_column'], axis=1)
        y = df[self.conf['target_column']]
        return X, y
    
    def load_session_from_file(self, path):
        with open(path, 'r') as file:
            self.conf = json.loads(file.read())
    
    def get_dataset(self):
        return pd.read_csv(self.conf['df_path'])
    
    def train_test_split(self, X, y):
        return train_test_split(X, y, test_size = float(self.conf['test_size']), random_state=int(self.conf['random_state']))
    
    def save(self):
        with open(self.name, 'w') as file:
            file.write(json.dumps(self.conf))
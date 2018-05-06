import json, os
from gui_helpers import gui_get_column, gui_get_file_path, gui_choose_option
from pandas_helpers import apply_preprocess_steps, gui_create_preprocess_step
import pandas as pd
from sklearn.cross_validation import train_test_split

ML_ACTIONS = ['regression', 'classification']
ML_MODELS = ['linear', 'svr', 'decision-tree', 'random-forest']

class SessionManager:

    conf = {}    
        
    def sanitize(self):
        """
        Use this function to set all the required states and not having to checkit all the time
        TODO: Implement
        """
        # self.conf['random_state'] = '0' # TODO: Move to sanitize
    
    def gui_start(self):
        print('gui_start')
        if input('start from previous session?[y/N]: ') == 'y':
            prev_session = input('enter previous session file path: ')
            self.load_session_from_file(prev_session)
        
        self.name = input('enter new session name: ')
            
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
            
        if 'action' not in self.conf.keys():
            self.conf['action'] = gui_choose_option(ML_ACTIONS, 'Choose a ML action')
            if self.conf['action'] != 'regression':
                print(' no es una regression!!!!! es: ', self.conf['action'])
            
        if 'model' not in self.conf.keys():
            self.conf['model'] = gui_choose_option(ML_MODELS, 'Choose a ML model')
            self.conf['model_conf'] = {}
            self.conf['model_conf']['random_state'] = 0
            if self.conf['model'] == 'svr':
                self.conf['model_conf']['kernel'] = gui_choose_option(['rbf'] = 'Choose a kernel')
            if self.conf['model'] == 'random-forest':
                self.conf['model_conf']['n_estimators'] = 10
            
        # Configure model
            
        self.sanitize()
        
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
    
    def get_action(self):
        return self.conf.get('action')
    
    def get_model(self):
        return self.conf.get('model')
    
    def get_model_conf(self):
        return self.conf.get('model_conf', {})
    
    def save(self):
        with open(self.name, 'w') as file:
            file.write(json.dumps(self.conf))
# Regression

# Importing the libraries
import numpy as np
import pandas as pd
from plot_helper import plot_2d_regression
from sklearn.cross_validation import train_test_split
import json
from pandas_helpers import apply_preprocess_steps, auto_one_hot_encoder, \
    create_preprocess_step
from gui_helpers import gui_get_column

data_preprocess_path = 'Salary_Data_data_preprocess.json'
dataset_path = './Part_02-Regression/Section_04-Simple_Linear_Regression/Salary_Data.csv'

data_preprocess_path = '50_Startups-data_preprocess.json'
dataset_path = './Part_02-Regression/Section_05-Multiple_Linear_Regression/50_Startups.csv'

# Importing the dataset
dataset = pd.read_csv(dataset_path)

# Load Preprocess Steps
try:
    with open(data_preprocess_path, 'r') as file:
        session_params = json.loads(file.read())
except FileNotFoundError as e:
    session_params = {}
    
preprocess_params = session_params.get('preprocess_params', [])
    
# Get Target Column by name
target_column = session_params.get('target_column')
if not target_column:
    target_column = gui_get_column(dataset)
    session_params['target_column'] = target_column
    
# Separate Target from Features
X = dataset.drop(target_column, axis=1)
y = dataset[target_column]

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)

# Preprocess Train Features
X_train = apply_preprocess_steps(preprocess_params, X_train)

    
# Create New Preprocess Feature Step
print(10*"=", 'Create Preprocess Step')
while True:
    if input('Do you wish to create an extra preprocess step [y/N]: ') != 'y':
        break
    
    X_train, step_params = create_preprocess_step(X_train)
    preprocess_params.append(step_params)
    
# Preprocess Test Features
X_test = apply_preprocess_steps(preprocess_params, X_test)

    
# Write Preprocess Steps
session_params['preprocess_params'] = preprocess_params
with open(data_preprocess_path, 'w') as file:
    file.write(json.dumps(session_params))


# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)

# Plot
plot_2d_regression(regressor, X_train, y_train)
plot_2d_regression(regressor, X_test, y_test)



import pandas as pd
from plot_helper import plot_2d_regression
from helpers import SessionManager

# dataset_path = './Part_02-Regression/Section_04-Simple_Linear_Regression/Salary_Data.csv'
# dataset_path = './Part_02-Regression/Section_05-Multiple_Linear_Regression/50_Startups.csv'


if input('start from previous session?[y/N]: ') == 'y':
    prev_session = input('enter previous session file path: ')
else:
    prev_session = None

session_name = input('enter new session name: ')

sm = SessionManager(session_name)
if prev_session:
    sm.load_session_from_file(prev_session)
sm.gui_start()

dataset = sm.get_dataset()

X, y = sm.separate_feature_from_target(dataset)

X_train, X_test, y_train, y_test = sm.train_test_split(X, y)

X_train = sm.apply_preprocess_steps(X_train)

x_train = sm.gui_create_preprocess_steps(X_train)
    
X_test = sm.apply_preprocess_steps(X_test)


sm.save()
prev_session = sm.name
    

# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)

# Plot
plot_2d_regression(regressor, X_train, y_train)
plot_2d_regression(regressor, X_test, y_test)



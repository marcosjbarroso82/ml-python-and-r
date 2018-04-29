# Regression

# Importing the libraries
import numpy as np
import pandas as pd
from plot_helper import plot_2d_regression

# Importing the dataset
dataset_path = './Part_02-Regression/Section_04-Simple_Linear_Regression/Salary_Data.csv'
dataset = pd.read_csv(dataset_path)
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)

# Feature Scaling
"""from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)"""

# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)

# Plot
plot_2d_regression(regressor, X_train, y_train)
plot_2d_regression(regressor, X_test, y_test)

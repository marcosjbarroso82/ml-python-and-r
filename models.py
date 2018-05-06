from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

class Regressor:
    
    def __init__(self, type, conf={}):
        self.type = type
        self.conf = conf
        if type == 'linear':
            self.regressor = LinearRegression()
        elif type == 'svr':
            self.regressor = SVR(**conf)
        elif type == 'decision-tree':
            self.regressor = DecisionTreeRegressor(**conf)
        elif type == 'random-forest':
            self.regressor = RandomForestRegressor(**conf)
        
    def pre_process(self, df):
        if self.type == 'linear' and self.conf['degree'] == 1 and len(df.columns) > 1:
            # Mutliple Linear Regression
            df.insert(0, 'ones', 1)
        elif self.type == 'linear' and self.conf['degree'] > 1:
            # Polinomial Linear Regression
            poly_reg = PolynomialFeatures(degree = self.conf['degree']) # TODO: poly_reg is a good name?
            df = poly_reg.fit_transform(df)
        return df
        
    def fit(self, X, y, transform=False):
        X = self.pre_process(X)
        self.regressor.fit(X, y)
        
    def predict(self, X):
        X = self.pre_process(X)
        return self.regressor.predict(X)
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

class Regressor:
    
    # TODO: Create a model conf
    def __init__(self, type, degree=1):
        self.type = type
        if type == 'linear':
            self.regressor = LinearRegression()
        elif type == 'svr':
            self.regressor = SVR(kernel = 'rbf') # TODO: Add more kernels
        elif type == 'decision-tree':
            self.regressor = DecisionTreeRegressor(random_state = 0) # TODO: Move random state to a proper place
        elif type == 'random-forest':
            self.regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
        
        # TODO: move degree to a model param
        self.degree = degree # used for polinomial regressions
        
    def pre_process(self, df):
        if self.type == 'linear' and self.degree == 1 and len(df.columns) > 1:
            # Mutliple Linear Regression
            df.insert(0, 'ones', 1)
        elif self.type == 'linear' and self.degree > 1:
            # Polinomial Linear Regression
            poly_reg = PolynomialFeatures(degree = self.degree) # TODO: poly_reg is a good name?
            df = poly_reg.fit_transform(df)
        return df
        
    def fit(self, X, y, transform=False):
        X = self.pre_process(X)
        self.regressor.fit(X, y)
        
    def predict(self, X):
        return self.regressor.predict(X)
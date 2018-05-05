from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

class Regressor:
    
    def __init__(self, type, degree=1):
        self.type = type
        if type == 'linear':
            self.regressor = LinearRegression()
        self.degree = degree # used for polinomial regressions
        
    def pre_process(self, df):
        if self.degree == 1 and len(df.columns) > 1:
            # Mutliple Linear Regression
            df.insert(0, 'ones', 1)
        elif self.degree > 1:
            # Polinomial Linear Regression
            poly_reg = PolynomialFeatures(degree = self.degree) # TODO: poly_reg is a good name?
            df = poly_reg.fit_transform(df)
        return df
        
    def fit(self, X, y, transform=False):
        X = self.pre_process(X)
        self.regressor.fit(X, y)
        
    def predict(self, X):
        return self.regressor.predict(X)
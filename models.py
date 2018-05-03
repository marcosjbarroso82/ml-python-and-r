from sklearn.linear_model import LinearRegression

class Regressor:
    
    def __init__(self, type):
        self.type = type
        if type == 'linear':
            self.regressor = LinearRegression()
            
    def fit(self, X, y):
        self.regressor.fit(X, y)
        
    def predict(self, X):
        return self.regressor.predict(X)
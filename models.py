from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

class MLModel:
    
    def __init__(self, type, conf={}):
        # TODO: Use more options for the models from the doc. Create a dictionary explaining them. Also specify defaults.
        self.type = type
        self.conf = conf
        if type == 'linear':
            self.model = LinearRegression()
        elif type == 'svr':
            self.model = SVR(kernel=conf['kernel'])
        elif type == 'decision-tree':
            self.model = DecisionTreeRegressor(random_state=conf['random_state'])
        elif type == 'random-forest':
            self.model = RandomForestRegressor(n_estimators=conf['n_estimators'], random_state=conf['random_state'])
        elif type == 'logistic-classifier':
            self.model = LogisticRegression(random_state=conf['random_state'])
        elif type == 'knn-classifier':
            self.model = KNeighborsClassifier(n_neighbors = 5) # TODO: Use more options from the doc
        elif type == 'svc':
            self.model = SVC(kernel = 'linear', random_state = 0)
        elif type == 'gaussian_naive_bayes':
            self.model = GaussianNB()
        elif type == 'decision-tree-classifier':
            self.model = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        elif type == 'random-forest-classifier':
            self.model = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
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
        self.model.fit(X, y)
        
    def predict(self, X):
        X = self.pre_process(X)
        return self.model.predict(X)
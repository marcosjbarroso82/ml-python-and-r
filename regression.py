from helpers import SessionManager
from models import Regressor
# dataset_path = './Part_02-Regression/Section_04-Simple_Linear_Regression/Salary_Data.csv'
# dataset_path = './Part_02-Regression/Section_05-Multiple_Linear_Regression/50_Startups.csv'
# dataset_path = './Part_02-Regression/Section_06-Polynomial_Regression/Position_Salaries.csv'
# dataset_path = './Part_02-Regression/Section_07-Support_Vector_Regression(SVR)/Position_Salaries.csv'
# dataset_path = './Part_02-Regression/Section_08-Decision_Tree_Regression/Position_Salaries.csv'

sm = SessionManager()
sm.gui_start()

dataset = sm.get_dataset()

X, y = sm.separate_feature_from_target(dataset)

X_train, X_test, y_train, y_test = sm.train_test_split(X, y)

X_train = sm.apply_preprocess_steps(X_train)
# TODO: Create more preprocess steps
X_train = sm.gui_create_preprocess_steps(X_train)
    
X_test = sm.apply_preprocess_steps(X_test)

# TODO: Implement the other models
if sm.get_action() == 'regression':
    model = Regressor(sm.get_model(), sm.get_model_conf())
    
model.fit(X_train, y_train)

# Predicting the Test set results
y_pred = model.predict(X_test)

# TODO: Log metrics
sm.save()
prev_session = sm.name

# Plot
# plot_2d_regression(regressor, X_train, y_train)
# plot_2d_regression(regressor, X_test, y_test)



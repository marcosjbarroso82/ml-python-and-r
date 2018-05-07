from helpers import SessionManager
from models import Regressor
# dataset_path = './Part_02-Regression/Section_04-Simple_Linear_Regression/Salary_Data.csv'
# dataset_path = './Part_02-Regression/Section_05-Multiple_Linear_Regression/50_Startups.csv'
# dataset_path = './Part_02-Regression/Section_06-Polynomial_Regression/Position_Salaries.csv'
# dataset_path = './Part_02-Regression/Section_07-Support_Vector_Regression(SVR)/Position_Salaries.csv'
# dataset_path = './Part_02-Regression/Section_08-Decision_Tree_Regression/Position_Salaries.csv'
# dataset_path = './Part_02-Regression/Section_09 -Random_Forest_Regression/Position_Salaries.csv'
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
elif sm.get_action() == 'classification':
    # TODO: Rename class for both Regression and Classification
    model = Regressor(sm.get_model(), sm.get_model_conf())
    
    # TODO: Move Feature Scaling to logic
    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
model.fit(X_train, y_train)

# Predicting the Test set results
y_pred = model.predict(X_test)

# TODO: Log metrics
sm.save()
prev_session = sm.name

if sm.get_action() == 'regression':
    # Plot
    # plot_2d_regression(regressor, X_train, y_train)
    # plot_2d_regression(regressor, X_test, y_test)
    pass
elif sm.get_action() == 'classification':
    # TODO: Move Graphics to helpers
    
    # Visualising the Training set results
    from matplotlib.colors import ListedColormap
    X_set, y_set = X_train, y_train
    X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                         np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
    plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                 alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                    c = ListedColormap(('red', 'green'))(i), label = j)
    plt.title('Logistic Regression (Training set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()
    
    # Visualising the Test set results
    from matplotlib.colors import ListedColormap
    X_set, y_set = X_test, y_test
    X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                         np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
    plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                 alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                    c = ListedColormap(('red', 'green'))(i), label = j)
    plt.title('Logistic Regression (Test set)')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    plt.legend()
    plt.show()


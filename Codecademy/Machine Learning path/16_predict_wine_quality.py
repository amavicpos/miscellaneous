# Regularization and hyperparameter tuning (C parameter) with logistic regression

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('utils/wine_quality.csv')
y = df['quality']
features = df.drop(columns=['quality'])

# 1. Data transformation
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(features)

# 2. Train-test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)

# 3. Fit a logistic regression classifier without regularization
from sklearn.linear_model import LogisticRegression

clf_no_reg = LogisticRegression(penalty='none')
clf_no_reg.fit(X_train, y_train)

# 4. Plot the coefficients
predictors = features.columns
coefficients = clf_no_reg.coef_.ravel()
coef = pd.Series(coefficients, predictors).sort_values()
coef.plot(kind='bar', title='Coefficients (no regularization)')
plt.tight_layout()
plt.show()
plt.clf()

# 5. Training and test performance
from sklearn.metrics import f1_score

y_pred_test = clf_no_reg.predict(X_test)
y_pred_train = clf_no_reg.predict(X_train)
print("F1 score for logistic regression, training data (no penalty):", f1_score(y_train, y_pred_train))
print("F1 score for logistic regression, test data (no penalty):", f1_score(y_test, y_pred_test))

# 6. Default Implementation (L2-regularized!)
clf_default = LogisticRegression()

# 7. Ridge Scores
clf_default.fit(X_train, y_train)
y_pred_train = clf_default.predict(X_train)
y_pred_test = clf_default.predict(X_test)
print("F1 score for logistic regression, training data (Ridge reg.):", f1_score(y_train, y_pred_train))
print("F1 score for logistic regression, test data (Ridge reg.):", f1_score(y_test, y_pred_test))

# 8. Coarse-grained hyperparameter tuning
training_array = []
test_array = []
C_array = [0.0001, 0.001, 0.01, 0.1, 1]
for C in C_array:
    model = LogisticRegression(C=C)
    model.fit(X_train, y_train)
    training_array.append(model.score(X_train, y_train))
    test_array.append(model.score(X_test, y_test))

# 9. Plot training and test scores as a function of C
plt.plot(C_array, training_array)
plt.plot(C_array, test_array)
plt.xlabel("C")
plt.ylabel("Score")
plt.xscale("log")
plt.legend(["Training", "Test"])
plt.show()

# 10. Making a parameter grid for GridSearchCV
C_array = np.logspace(-4, -2, 100)
tuning_C = {'C': C_array}

# 11. Implementing GridSearchCV with l2 penalty
from sklearn.model_selection import GridSearchCV

clf_gs = LogisticRegression()
gs = GridSearchCV(clf_gs, param_grid=tuning_C, scoring='f1', cv=5)
gs.fit(X_train, y_train)

# 12. Optimal C value and the score corresponding to it
optimal_C = gs.best_params_['C']
best_score = gs.best_score_

# 13. Validating the "best classifier"
clf_best = LogisticRegression(C=optimal_C)
clf_best.fit(X_train, y_train)
y_pred_best = clf_best.predict(X_test)
print("F1 score of logistic regression with optimal C, test data (Ridge reg.):", f1_score(y_test, y_pred_best))

# 14. Implement L1 hyperparameter tuning with LogisticRegressionCV
from sklearn.linear_model import LogisticRegressionCV

clf_l1 = LogisticRegressionCV(Cs=np.logspace(-2, 2, 10), cv=5, penalty='l1', solver='liblinear', scoring='f1')
clf_l1.fit(X, y)

# 15. Optimal C value and corresponding coefficients
print("Optimal_C with Lasso reg.:", clf_l1.C_, "\nCoefficients:", clf_l1.coef_.ravel())

# 16. Plotting the tuned L1 coefficients
coefficients = clf_l1.coef_.ravel()
coef = pd.Series(coefficients, predictors).sort_values()

plt.figure(figsize=(12, 8))
coef.plot(kind='bar', title='Coefficients for tuned L1')
plt.tight_layout()
plt.show()

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LassoCV
from sklearn.linear_model import RidgeCV

df = pd.read_csv("transformierte_normierte_daten.csv")

rows, cols = df.shape
print(f"Datensatzgröße: {rows} Zeilen, {cols} Variablen (inklusive Zielvariable)")

y = df['time_to_fail']
X = df.drop(columns=['time_to_fail'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Stichprobe
sample_frac = 0.1  # 10% der Daten
X_sample, _, y_sample, _ = train_test_split(X_train, y_train, train_size=sample_frac, random_state=42)

param_dist = {
    'n_estimators': [100, 300, 500],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 10, 50],
    'min_samples_leaf': [1, 4, 10],
    'max_features': ['auto', 'sqrt', 'log2']
}

rand_search = RandomizedSearchCV(
    estimator=RandomForestRegressor(n_jobs=-1, random_state=42),
    param_distributions=param_dist,
    n_iter=20,
    cv=3,
    scoring='neg_mean_squared_error',
    verbose=2,
    n_jobs=-1,
    random_state=42
)

print("Starte Hyperparameter-Tuning mit Stichprobe...")
rand_search.fit(X_sample, y_sample)

print("Beste Parameter:", rand_search.best_params_)

best_rf = rand_search.best_estimator_

importance_df = pd.DataFrame({
    'Variable': X.columns,
    'Importance': best_rf.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("Wichtigste Variablen laut Random Forest:")
print(importance_df)

top_vars = importance_df['Variable'].head(10).tolist()

print("Ausgewählte Variablen für das finale Modell:", top_vars)


# LASSO mit Cross-Validation
lasso = LassoCV(cv=5, random_state=42)
lasso.fit(X_train, y_train)

lasso_importance = pd.Series(lasso.coef_, index=X.columns)
important_vars_lasso = lasso_importance[lasso_importance != 0].sort_values(ascending=False)

print("Wichtigste Variablen laut LASSO:")
print(important_vars_lasso)


# Ridge Regression mit Cross-Validation
ridge = RidgeCV(cv=5)
ridge.fit(X_train, y_train)

ridge_importance = pd.Series(ridge.coef_, index=X.columns)
important_vars_ridge = ridge_importance.abs().sort_values(ascending=False)

print("Wichtigste Variablen laut Ridge (L2):")
print(important_vars_ridge)

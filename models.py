from unittest import result
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR # Support Vector Regression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Linear Regression': LinearRegression(),
        'Support Vector Regression': SVR(kernel='linear')
    }

def evaluate_models(X_train, X_test, y_train, y_test):

    results = {}
    
    for name, model in models.items():
        # Treinar o modelo
        model.fit(X_train, y_train)

        # Fazer previsões
        y_pred = model.predict(X_test)

        # Calcular métricas
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results[name] = {
            'MAE': mae,
            'R²': r2
        }

    return results

print("Métricas dos Modelos:", result)
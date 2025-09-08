from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from models import evaluate_models

def identify_prerequisite_issues(df, pre_reqs, threshold=5.0):
    recommendations = {}
    metrics_summary = {}

    # Iteração sobre Disciplinas
    for subject, reqs in pre_reqs.items():
        X = df[reqs]
        y = df[subject]

        # Dividir os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Avaliar modelos e coletar métricas
        metrics = evaluate_models(X_train, X_test, y_train, y_test)
        metrics_summary[subject] = metrics

        # Codificar variáveis categóricas
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        preprocessor = ColumnTransformer(transformers=[('cat', OneHotEncoder(drop='first'), categorical_cols)], remainder='passthrough')
        X_transformed = preprocessor.fit_transform(X)

        # Treinar o modelo Random Forest
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train, y_train)

        # Verificar a importância dos pré-requisitos
        importance = model.feature_importances_
        importance_dict = {req: imp for req, imp in zip(reqs, importance)}

        # Recomendações
        for _, row in df.iterrows():
            if row[subject] < threshold:
                aluno = row["Aluno"]
                if aluno not in recommendations:
                    recommendations[aluno] = []

                for req in reqs:
                    if req not in recommendations[aluno]:
                        recommendations[aluno].append((req, importance_dict[req]))

    # Ordenação das recomendações
    for aluno in recommendations:
        recommendations[aluno] = sorted(recommendations[aluno], key=lambda x: x[1], reverse=True)

    return recommendations, metrics_summary

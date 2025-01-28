import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Charger les données
def entrainement(df):
    data = pd.read_csv(df)

    # Convertir la date en datetime
    data['date'] = pd.to_datetime(data['date'])

    # Extraire des informations temporelles
    data['jour'] = data['date'].dt.day
    data['mois'] = data['date'].dt.month
    data['jour_semaine'] = data['date'].dt.weekday  # 0=Monday, 6=Sunday
    data['annee'] = data['date'].dt.year

    # Encoder la colonne 'quartier'
    label_encoder = LabelEncoder()
    data['quartier'] = label_encoder.fit_transform(data['quartier'])+1

    # Redéfinir X et y
    X = data[['temperature', 'humidite', 'pluie_intensite_max'
              ,
              'pluie_totale', 'sismicite', 'concentration_gaz', 'quartier', 'mois', 'annee'
                ]]  # Inclure les nouvelles variables temporelles
    y = data['catastrophe']  # Remplace 'inondation' par ta colonne cible

    # Diviser les données en jeux d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Entraîner un modèle multi-sortie
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

    rf_model.fit(X_train, y_train)

    # Prédictions
    y_pred = rf_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Précision globale : {accuracy:.2f}")

    # Matrice de confusion
    print("\nMatrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns)
    feature_importances.nlargest(10).plot(kind='barh')
    plt.title('Feature Importance')
    plt.show()


    # Sauvegarder le modèle entraîné
    joblib.dump(rf_model, 'random_forest_model.pkl')
    joblib.dump(label_encoder, 'label_encoder.pkl')  # Sauvegarder aussi l'encodeur
    print("Modèle et encodeur sauvegardés")


entrainement('catastrophes_naturelles_data_cleaned.csv')
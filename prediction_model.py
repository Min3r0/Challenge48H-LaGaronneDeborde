import pandas as pd
import joblib

# Charger le modèle et l'encodeur
rf_model = joblib.load('random_forest_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')
def prediction(df):
# Charger le fichier de données pour la prédiction
    nouveaux_data = pd.read_csv(df)

# Convertir la date en datetime
    nouveaux_data['date'] = pd.to_datetime(nouveaux_data['date'])

    # Extraire les informations temporelles
    nouveaux_data['jour'] = nouveaux_data['date'].dt.day
    nouveaux_data['mois'] = nouveaux_data['date'].dt.month
    nouveaux_data['jour_semaine'] = nouveaux_data['date'].dt.weekday
    nouveaux_data['annee'] = nouveaux_data['date'].dt.year

    # Encoder la colonne 'quartier'
    nouveaux_data['quartier'] = label_encoder.transform(nouveaux_data['quartier'])+1

    # Redéfinir X pour la prédiction
    X_nouveaux = nouveaux_data[['temperature', 'humidite',  'pluie_intensite_max',
                                 'pluie_totale', 'sismicite', 'concentration_gaz', 'quartier',
                                  'mois', 'annee']]

    # Prédire les catastrophes
    predictions = rf_model.predict(X_nouveaux)

    # Obtenir les probabilités associées à chaque classe
    proba_predictions = rf_model.predict_proba(X_nouveaux)

    # Ajouter les prédictions comme nouvelles colonnes
    nouveaux_data['catastrophe_predite'] = predictions
    nouveaux_data['proba_aucune'] = proba_predictions[:, 0]  # Probabilité de classe 0 (aucune catastrophe)
    nouveaux_data['proba_seisme'] = proba_predictions[:, 1]  # Probabilité de classe 1 (séisme)
    nouveaux_data['proba_inondation'] = proba_predictions[:, 2]  # Probabilité de classe 2 (inondation)
    nouveaux_data['proba_seisme_inondation'] = proba_predictions[:, 3]  # Probabilité de classe 3 (séisme & inondation)
    nouveaux_data = nouveaux_data.drop(columns=['jour'])
    nouveaux_data = nouveaux_data.drop(columns=['mois'])
    nouveaux_data = nouveaux_data.drop(columns=['jour_semaine'])
    nouveaux_data = nouveaux_data.drop(columns=['annee'])

    # Sauvegarder les résultats dans un fichier CSV
    nouveaux_data.to_csv('resultats_predictions_probabilites.csv', index=False)

    print("Prédictions avec probabilités enregistrées dans 'resultats_predictions_probabilites.csv'")


prediction('catastrophes_naturelles_data_cleaned.csv')
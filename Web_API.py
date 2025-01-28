from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

data = pd.read_csv("data.csv")


# Route pour obtenir toutes les données en JSON
@app.route('/data', methods=['GET'])
def get_all_data():
    result = data.to_dict(orient='records')
    return jsonify(result)


# Route pour obtenir une ligne spécifique par ID
@app.route('/data/<int:record_id>', methods=['GET'])
def get_data_by_id(record_id):
    record = data[data['id'] == record_id]
    if record.empty:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record.to_dict(orient='records')[0])


# Route pour filtrer les données par colonne (ex: date, type de catastrophe, etc.)
@app.route('/data/filter', methods=['GET'])
def filter_data():
    column = request.args.get('column')
    value = request.args.get('value')

    if column not in data.columns:
        return jsonify({"error": f"Column '{column}' not found"}), 400

    # Obtenir le type de la colonne pour comparaison
    col_type = data[column].dtype

    # Convertir la valeur en fonction du type de la colonne
    if col_type == 'int64':
        try:
            value = int(value)
        except ValueError:
            return jsonify({"error": f"Value '{value}' is not a valid integer"}), 400
    elif col_type == 'float64':
        try:
            value = float(value)
        except ValueError:
            return jsonify({"error": f"Value '{value}' is not a valid float"}), 400
    elif col_type == 'bool':
        if value.lower() in ['true', '1']:
            value = True
        elif value.lower() in ['false', '0']:
            value = False
        else:
            return jsonify({"error": f"Value '{value}' is not a valid boolean"}), 400

    filtered_data = data[data[column] == value]

    if filtered_data.empty:
        return jsonify({"error": "No matching records found"}), 404

    return jsonify(filtered_data.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

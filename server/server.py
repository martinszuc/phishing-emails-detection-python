import logging
from logging.handlers import RotatingFileHandler

# Configuration for logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('federated_learning.log', maxBytes=10000, backupCount=3)
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import numpy as np
import json
import os
import gzip

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///federated_learning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models
class Client(db.Model):
    id = db.Column(db.String(255), primary_key=True)  # Updated to String
    last_update = db.Column(db.DateTime, nullable=True)

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(255), db.ForeignKey('client.id'), nullable=False)  # Updated to String
    weights = db.Column(db.Text, nullable=False)  # Storing weights as JSON text

def initialize_database():
    """Ensure the database and tables are created."""
    with app.app_context():
        db.create_all()


@app.route('/upload_weights', methods=['POST'])
def upload_weights():
    try:
        client_id = request.form['client_id']
        file = request.files['weights_file']
        
        if not client_id or not file:
            return jsonify({"error": "Missing client_id or weights file"}), 400
        
        
        # Process the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join("/tmp", filename)  # Temporary save location, adjust as needed
        file.save(filepath)

        # Decompress the file
        with gzip.open(filepath, 'rb') as f:
            weights_data = f.read()
        
        # Convert binary data to a format that can be saved in DB (e.g., JSON string or directly saving binary data)
        # This example assumes the decompressed data is JSON formatted
        weights_json = weights_data.decode('utf-8')

        logger.info(f"Received weights file for upload from client_id: {client_id}")
        
        client = Client.query.get(client_id)
        if not client:
            client = Client(id=client_id)
            db.session.add(client)

        weight_entry = Weight.query.filter_by(client_id=client_id).first()
        if weight_entry:
            # Update existing weights for this client
            weight_entry.weights = weights_json
        else:
            # Create a new weight entry for this client
            weight_entry = Weight(client_id=client_id, weights=weights_json)
            db.session.add(weight_entry)
        
        db.session.commit()

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred during weight file upload"}), 500


@app.route('/get_weights', methods=['GET'])
def get_weights():
    try:
        weights_query = Weight.query.all()
        if not weights_query:
            return jsonify({"error": "No weights available"}), 404
        
        # Assuming weights are stored as JSON arrays
        weights_list = [json.loads(weight.weights) for weight in weights_query]
        
        # Convert lists to NumPy arrays for averaging
        numeric_weights = [np.array(weight) for weight in weights_list]
        
        # Calculate the average across all arrays
        averaged_weights = np.mean(numeric_weights, axis=0).tolist()

        return jsonify({"weights": json.dumps(averaged_weights)}), 200
    except Exception as e:
        return jsonify({"error": "Aggregation error"}), 500


@app.route('/check', methods=['GET'])
def check_server():
    return jsonify({"status": "Server is up and running!"}), 200

if __name__ == "__main__":
    initialize_database()  # Ensure DB is initialized within an app context
    app.run(debug=True, host='0.0.0.0', port=5000)

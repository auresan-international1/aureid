import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Initialize Flask App
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully.")
except Exception as e:
    print(f"❌ Error initializing Firebase: {e}")

# --- NEW ROUTE TO SERVE THE WEBSITE ---
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# --- EXISTING API ROUTE ---
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        name = data.get('name')
        phone = data.get('phone')

        if not name or not phone:
            return jsonify({"error": "Name and phone are required"}), 400

        doc_ref = db.collection('leads').add({
            'name': name,
            'phone': phone,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'status': 'new'
        })

        print(f"✅ Lead saved: {name} - {phone}")
        return jsonify({"message": "Order received successfully!", "id": doc_ref[1].id}), 201

    except Exception as e:
        print(f"❌ Error saving to Firebase: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
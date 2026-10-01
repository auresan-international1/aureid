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
        productname = data.get('productname', 'DiaFormula')

        if not name or not phone:
            return jsonify({"error": "Name and phone are required"}), 400

        # Generate auto-incrementing ID (DA-001, DA-002, etc.)
        counter_ref = db.collection('counters').document('leads')
        counter_doc = counter_ref.get()
        if counter_doc.exists:
            count = counter_doc.to_dict().get('count', 0) + 1
        else:
            count = 1
        
        lead_id = f"DA-{count:03d}"
        
        # Update counter
        counter_ref.set({'count': count})

        # Optional fields from client
        priority = data.get('priority', 'normal')
        source = data.get('source', 'website')
        status = data.get('status', 'new')

        # Allow client to supply created_at/updated_at (ISO string), otherwise use SERVER_TIMESTAMP
        created_at = data.get('created_at') if data.get('created_at') else firestore.SERVER_TIMESTAMP
        updated_at = data.get('updated_at') if data.get('updated_at') else firestore.SERVER_TIMESTAMP

        add_result = db.collection('leads').add({
            'id': lead_id,
            'name': name,
            'phone': phone,
            'productname': productname,
            'priority': priority,
            'source': source,
            'status': status,
            'created_at': created_at,
            'updated_at': updated_at
        })

        # db.collection().add() may return a tuple in different orders depending on
        # firestore client version. Find the DocumentReference (has attribute 'id').
        if isinstance(add_result, tuple) or isinstance(add_result, list):
            if hasattr(add_result[0], 'id'):
                doc_ref = add_result[0]
            elif len(add_result) > 1 and hasattr(add_result[1], 'id'):
                doc_ref = add_result[1]
            else:
                # Fallback: pick first element
                doc_ref = add_result[0]
        else:
            # If add_result is a DocumentReference
            doc_ref = add_result

        print(f"✅ Lead saved: {lead_id} - {name} - {phone} - {productname}")
        return jsonify({"message": "Order received successfully!", "id": doc_ref.id, "lead_id": lead_id}), 201

    except Exception as e:
        print(f"❌ Error saving to Firebase: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
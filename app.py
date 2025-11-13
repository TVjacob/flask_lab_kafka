# app.py
from flask import Flask, request, jsonify
from models import db, LabBatch, LabSample, AuditLog
from kafka_producer import emit_event
from flask_cors import CORS  # <-- import CORS

import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  # <-- enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab_workflow.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/create_batch', methods=['POST'])
def create_batch():
    data = request.json
    batch_id = str(uuid.uuid4())
    batch = LabBatch(batch_id=batch_id, patient_name=data['patient_name'],
                     test_type=data['test_type'], status='Requested', priority=data.get('priority', 'High'))
    db.session.add(batch)
    db.session.commit()

    # Emit Kafka event
    emit_event('lab_request_created', {"batch_id": batch_id, "patient_name": batch.patient_name, "status": batch.status})
    return jsonify({"message": "Batch created", "batch_id": batch_id})

@app.route('/update_status/<batch_id>', methods=['POST'])
def update_status(batch_id):
    data = request.json
    batch = LabBatch.query.filter_by(batch_id=batch_id).first()
    if not batch:
        return jsonify({"error": "Batch not found"}), 404

    batch.status = data['status']
    db.session.commit()

    emit_event('audit_trail', {"batch_id": batch_id, "action_type": "Status Update", "user": data.get("user", "system"),
                               "timestamp": str(datetime.utcnow()), "details": f"Status changed to {batch.status}"})
    emit_event('customer_notification', {"batch_id": batch_id, "status": batch.status, "customer_id": data.get("customer_id")})
    return jsonify({"message": f"Status updated to {batch.status}"})

# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class LabBatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(50), unique=True)
    patient_name = db.Column(db.String(100))
    test_type = db.Column(db.String(100))
    status = db.Column(db.String(50))  # Requested, Approved, Sample Collected, etc.
    priority = db.Column(db.String(10))  # High, Medium, Low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LabSample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(50))
    sample_id = db.Column(db.String(50))
    collected_by = db.Column(db.String(100))
    collection_time = db.Column(db.DateTime)
    analysis_status = db.Column(db.String(50))  # Pending, Analyzed, Approved
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(50))
    sample_id = db.Column(db.String(50))
    action_type = db.Column(db.String(50))
    user = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(255))

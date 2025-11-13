# app.py
from flask import Flask, request, jsonify
from models import db, LabBatch, LabSample, AuditLog
from kafka_producer import emit_event
from flask_cors import CORS  # <-- import CORS
import tempfile
import zipfile
import os
from flask import send_file
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO


app = Flask(__name__)
CORS(app)  # <-- enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab_workflow.db'
db.init_app(app)

with app.app_context():
    db.create_all()



# UPLOAD_FOLDER = "uploads"
# RESULT_FOLDER = "results"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(RESULT_FOLDER, exist_ok=True)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/upload_files', methods=['POST'])
def upload_files():
    files = request.files
    saved_files = []

    # Check and save uploaded files
    for ftype, max_size in [('xml', 1*1024), ('json', 1*1024), ('image', 50*1024), ('pdf', 10*1024)]:
        if ftype not in files:
            return jsonify({"error": f"{ftype} file missing"}), 400

        file = files[ftype]
        if len(file.read()) > max_size:
            return jsonify({"error": f"{ftype} file exceeds max size"}), 400
        file.seek(0)

        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        saved_files.append(path)

    # Emit Kafka event for upload started
    batch_id = str(uuid.uuid4())
    emit_event('file_upload_initiated', {"batch_id": batch_id, "files": [os.path.basename(f) for f in saved_files]})

    # Create ZIP in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for i in range(50):
            # Generate lightweight PDF
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=(200, 200))  # small page
            c.setFont("Helvetica", 6)
            c.drawString(10, 100, f"Report {i} batch {batch_id}")
            c.showPage()
            c.save()
            pdf_buffer.seek(0)

            # Check PDF size
            if pdf_buffer.getbuffer().nbytes > 20*1024:
                return jsonify({"error": f"PDF {i} exceeds 20 KB"}), 400

            pdf_name = f"report_{i}.pdf"
            z.writestr(pdf_name, pdf_buffer.read())

    zip_buffer.seek(0)

    # Check total ZIP size
    if zip_buffer.getbuffer().nbytes > 50*1024:
        return jsonify({"error": "ZIP exceeds 50 KB"}), 400

    # Save ZIP to temp file and send
    zip_path = tempfile.NamedTemporaryFile(delete=False, suffix=".zip").name
    with open(zip_path, 'wb') as f:
        f.write(zip_buffer.read())

    # Emit Kafka event for processing done
    emit_event('file_processing_done', {"batch_id": batch_id, "zip": os.path.basename(zip_path)})

    return send_file(
        zip_path,
        as_attachment=True,
        download_name="results.zip",
        mimetype="application/zip"
    )

# @app.route('/upload_files', methods=['POST'])
# def upload_files():
#     files = request.files
#     job_id = str(uuid.uuid4())
#     upload_paths = {}cle

#     for key in ['xml', 'json', 'image', 'pdf']:
#         if key not in files:
#             return jsonify({"error": f"{key} file missing"}), 400
#         file = files[key]
#         filename = f"{job_id}_{secure_filename(file.filename)}"
#         path = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(path)
#         upload_paths[key] = path

#     # Emit Kafka event for processing
#     emit_event("file_upload_requested", {"job_id": job_id, "files": upload_paths})

#     return jsonify({"message": "Files uploaded successfully", "job_id": job_id})

@app.route('/download_result/<job_id>', methods=['GET'])
def download_result(job_id):
    path = os.path.join(RESULT_FOLDER, f"{job_id}.zip")
    if not os.path.exists(path):
        return jsonify({"error": "Result not ready"}), 404
    return send_file(path, as_attachment=True)

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

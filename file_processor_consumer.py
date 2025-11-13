import os, io, zipfile, time
from confluent_kafka import Consumer
from kafka_producer import emit_event
from PyPDF2 import PdfWriter

consumer = Consumer({
    "bootstrap.servers": "kafka1:9092",
    "group.id": "file_processor_group",
    "auto.offset.reset": "earliest"
})

consumer.subscribe(["file_upload_requested","file_processing_done"])

def create_zip(job_id):
    # Simulate processing delay (~4 min = shorten for demo)
    time.sleep(5)

    result_dir = "results"
    os.makedirs(result_dir, exist_ok=True)
    zip_path = os.path.join(result_dir, f"{job_id}.zip")

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for i in range(1, 51):
            pdf_bytes = io.BytesIO()
            pdf = PdfWriter()
            pdf.add_blank_page(width=200, height=200)
            pdf.write(pdf_bytes)
            pdf_bytes.seek(0)
            zipf.writestr(f"result_{i}.pdf", pdf_bytes.read())

    return zip_path

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error:", msg.error())
        continue

    data = eval(msg.value().decode())
    job_id = data.get("job_id")
    zip_path = create_zip(job_id)

    emit_event("file_processing_completed", {
        "job_id": job_id,
        "zip_path": zip_path,
        "status": "done"
    })

consumer.close()

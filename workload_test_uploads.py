import asyncio
import aiohttp
import json
import random
import string
from aiohttp import FormData

UPLOAD_URL = "http://localhost:5080/upload_files"  # your Flask endpoint

# Generate fake small files of specified size (bytes)
def fake_file(name, size_kb):
    content = ''.join(random.choices(string.ascii_letters + string.digits, k=size_kb * 1024))
    return name, content.encode()

async def upload_one(session, idx):
    try:
        form = FormData()

        # Simulate the four file types with approximate sizes
        # form.add_field('xml', fake_file(f"file_{idx}.xml", 1)[1], filename=f"file_{idx}.xml", content_type='application/xml')
        # form.add_field('json_file', fake_file(f"file_{idx}.json", 1)[1], filename=f"file_{idx}.json", content_type='application/json')
        # form.add_field('image_file', fake_file(f"file_{idx}.jpg", 50)[1], filename=f"file_{idx}.jpg", content_type='image/jpeg')
        # form.add_field('pdf_file', fake_file(f"file_{idx}.pdf", 10)[1], filename=f"file_{idx}.pdf", content_type='application/pdf')
        form.add_field('xml', fake_file(f"file_{idx}.xml", 1)[1], filename=f"file_{idx}.xml", content_type='application/xml')
        form.add_field('json', fake_file(f"file_{idx}.json", 1)[1], filename=f"file_{idx}.json", content_type='application/json')
        form.add_field('image', fake_file(f"file_{idx}.jpg", 50)[1], filename=f"file_{idx}.jpg", content_type='image/jpeg')
        form.add_field('pdf', fake_file(f"file_{idx}.pdf", 10)[1], filename=f"file_{idx}.pdf", content_type='application/pdf')


        async with session.post(UPLOAD_URL, data=form) as resp:
            if resp.status == 200:
                data = await resp.json()
                print(f"[OK {idx}] -> {data.get('message')}")
            else:
                print(f"[ERR {idx}] Status {resp.status}")
    except Exception as e:
        print(f"[EXC {idx}] {e}")

async def main():
    total_requests = 2000
    concurrency = 100  # number of simultaneous uploads
    connector = aiohttp.TCPConnector(limit=concurrency)
    timeout = aiohttp.ClientTimeout(total=120)  # seconds

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [upload_one(session, i) for i in range(total_requests)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

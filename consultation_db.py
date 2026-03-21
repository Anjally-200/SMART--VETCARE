import json

FILE = "consultations.json"

def load_requests():
    with open(FILE, "r") as f:
        return json.load(f)

def save_request(request):
    data = load_requests()
    data.append(request)

    with open(FILE, "w") as f:
        json.dump(data, f)

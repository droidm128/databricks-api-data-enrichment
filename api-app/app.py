from flask import Flask, jsonify, request
from faker import Faker
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per second"]
)
fake = Faker()
request_counter = {'count': 0}

@app.route('/test', methods=['GET'])
@limiter.limit("5 per second")
def get_person():
    """Endpoint to get a random person's information.
    It accepts a 'login' query parameter and returns a JSON object with the person's details.
    Every 3 requests, it returns an error.
    """
    login = request.args.get('login', '')
    request_counter['count'] += 1
    if request_counter['count'] % 3 == 0:
        return jsonify({"error": "Triggered every 3 requests."}), 500
    person = {
        "login": login,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "username": fake.user_name(),
        "address": fake.address(),
        "phone": fake.phone_number(),
    }
    return jsonify(person)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) 
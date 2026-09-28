from flask import Flask, jsonify
import os

app = Flask(__name__)

def load_users():
    users = {}
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'users.txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 4:
                    uid, name, phone, address = parts
                    users[phone.strip()] = {
                        'id': uid.strip(),
                        'name': name.strip(),
                        'phone': phone.strip(),
                        'address': address.strip()
                    }
    except Exception as e:
        print(f"Error loading users: {e}")
    return users


@app.route('/')
def home():
    users = load_users()
    return jsonify({
        'status': 'ok',
        'message': 'API is running',
        'total_users': len(users),
        'usage': '/api/<phone_number>',
        'example': '/api/9000000001',
        'all_users': '/api/all'
    })


@app.route('/api/<phone>')
def get_user(phone):
    users = load_users()
    phone = phone.strip().replace(' ', '').replace('-', '')
    if phone.startswith('+91'):
        phone = phone[3:]
    elif phone.startswith('91') and len(phone) == 12:
        phone = phone[2:]

    user = users.get(phone)

    if user:
        return jsonify({'status': 'ok', 'data': user})
    else:
        return jsonify({
            'status': 'not_found',
            'message': 'Number not found',
            'phone': phone
        }), 404


@app.route('/api/all')
def get_all():
    users = load_users()
    return jsonify({
        'status': 'ok',
        'total': len(users),
        'data': list(users.values())
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

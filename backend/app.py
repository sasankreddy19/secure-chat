from flask import Flask, send_from_directory, abort
from flask_socketio import SocketIO, emit
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

app = Flask(__name__, static_folder='frontend')
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}
private_keys = {}
public_keys = {}

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_message(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except FileNotFoundError:
        abort(404, description="index.html not found in frontend directory")
    except Exception as e:
        abort(500, description=f"Server error: {str(e)}")

@socketio.on('register')
def handle_register(data):
    username = data.get('username')
    if not username or not isinstance(username, str):
        emit('error', {'message': 'Valid username is required'})
        return
    if username in users:
        emit('error', {'message': f'Username "{username}" already exists. Please choose another or login.'})
        return
    try:
        private_key, public_key = generate_key_pair()
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        private_keys[username] = private_key
        public_keys[username] = public_key_pem
        users[username] = {'public_key': public_key_pem}

        emit('register_success', {'username': username, 'public_key': public_key_pem})
        print(f"Registered user: {username} with public key: {public_key_pem[:50]}...")
    except Exception as e:
        emit('error', {'message': f'Registration failed: {str(e)}'})
        print(f"Registration error for {username}: {e}")

@socketio.on('login')
def handle_login(data):
    username = data.get('username')
    if not username or not isinstance(username, str):
        emit('error', {'message': 'Valid username is required'})
        return
    try:
        if username in public_keys:
            public_key_pem = public_keys[username]
            emit('login_success', {'username': username, 'public_key': public_key_pem})
            print(f"User logged in: {username} with public key: {public_key_pem[:50]}...")
        else:
            emit('error', {'message': 'Username not found. Please register.'})
            print(f"Login failed: Username '{username}' not found.")
    except Exception as e:
        emit('error', {'message': f'Login failed: {str(e)}'})
        print(f"Login error for {username}: {e}")

@socketio.on('send_message')
def handle_send_message(data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    if not all([sender, receiver, message]) or not all(isinstance(x, str) for x in [sender, receiver, message]):
        emit('error', {'message': 'Valid sender, receiver, and message are required'})
        return
    try:
        if receiver in public_keys:
            receiver_public_key = serialization.load_pem_public_key(
                public_keys[receiver].encode(),
                backend=default_backend()
            )
            encrypted_msg = encrypt_message(receiver_public_key, message)
            emit('new_message', {'sender': sender, 'message': encrypted_msg}, room=receiver)
        else:
            emit('error', {'message': 'Receiver not found'})
    except Exception as e:
        emit('error', {'message': f'Message failed: {str(e)}'})

@socketio.on('connect')
def handle_connect():
    emit('connected', {'message': 'Connected to SecureChat'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)

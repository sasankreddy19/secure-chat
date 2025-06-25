from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

app = Flask(__name__, static_folder='frontend', template_folder='frontend')
socketio = SocketIO(app, cors_allowed_origins="*")

# Store user public keys and sessions
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
    return render_template('index.html')

@socketio.on('register')
def handle_register(data):
    username = data.get('username')  # Use .get() to avoid KeyError if data is malformed
    if not username:
        emit('error', {'message': 'Username is required'})
        return
    private_key, public_key = generate_key_pair()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    private_keys[username] = private_key
    public_keys[username] = public_key_pem
    users[username] = {'public_key': public_key_pem}
    emit('register_success', {'username': username, 'public_key': public_key_pem})

@socketio.on('send_message')
def handle_send_message(data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    if not all([sender, receiver, message]):
        emit('error', {'message': 'Sender, receiver, and message are required'})
        return
    if receiver in public_keys:
        encrypted_msg = encrypt_message(serialization.load_pem_public_key(public_keys[receiver].encode()), message)
        emit('new_message', {'sender': sender, 'message': encrypted_msg}, room=receiver)
    else:
        emit('error', {'message': 'Receiver not found'})

@socketio.on('connect')
def handle_connect():
    emit('connected', {'message': 'Connected to SecureChat'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Heroku sets PORT, default to 5000 for local
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
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

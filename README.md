
# SecureChat: End-to-End Encrypted Messaging

[SecureChat Screenshot]
![Screenshot 2025-06-27 130853](https://github.com/user-attachments/assets/2e96de60-3038-4a9f-a94a-9369da54922e)


SecureChat is a minimalist web-based chat application designed with a focus on end-to-end encryption. It leverages RSA for key pair generation and encryption, ensuring that messages are secure from the sender to the intended receiver. Built with Flask-SocketIO for real-time communication and React (via Babel) for a dynamic frontend, SecureChat provides a basic yet powerful demonstration of secure messaging principles.

## ✨ Features

*   **End-to-End Encryption (E2EE):** Messages are encrypted using the receiver's RSA public key, ensuring only the intended recipient can decrypt and read them.
*   **RSA-2048 Key Pair Generation:** Each user generates a unique 2048-bit RSA key pair upon registration.
*   **Real-time Communication:** Powered by Socket.IO for instant message delivery.
*   **Simple User Interface:** A clean and intuitive interface built with React and Tailwind CSS.
*   **Basic User Registration/Login:** Users can register with a username, which generates their cryptographic keys. A basic "login" mechanism allows re-associating with existing keys (though not persistent across sessions without further development).
*   **Python Backend:** Robust and secure backend built with Flask and `cryptography` library.

## 🚀 Technologies Used

**Frontend:**
*   **React:** JavaScript library for building user interfaces.
*   **Babel:** Used for JSX transformation in the browser.
*   **Tailwind CSS:** A utility-first CSS framework for rapid UI development.
*   **Socket.IO Client:** For real-time, bidirectional communication.

**Backend:**
*   **Python 3.x**
*   **Flask:** A lightweight WSGI web application framework.
*   **Flask-SocketIO:** Integrates Socket.IO with Flask.
*   **Cryptography:** Python library for cryptographic recipes and primitives (RSA, AES).
*   **Gunicorn (optional, for production):** WSGI HTTP Server.
*   **Eventlet (optional, for production):** Concurrent networking library.

## 📦 Installation & Setup

Follow these steps to get SecureChat up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/SecureChat.git
cd SecureChat

## 2. 🖥️ Backend Setup (Python)

It's recommended to use a **virtual environment**.

### ▶️ Create & Activate Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### ▶️ Navigate to the Backend Directory

> *(Assuming **`app.py`** is in a **`backend`** folder. If it's in root, skip this step.)*

```bash
cd backend  # Adjust this path if needed
```

### ▶️ Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### ✅ `requirements.txt` contents:

```
flask
flask-socketio
cryptography
gunicorn
eventlet
```

---

## 3. 🌐 Frontend Setup

No separate build step is needed.

The frontend `index.html` includes:

- React
- ReactDOM
- Babel
- Tailwind CSS\
  **All via CDNs**, simplifying local development (no `npm install` or `build` needed).

---

## ▶️ How to Run

### 1. Start the Backend Server

Make sure your virtual environment is activated and you're in the same directory as `app.py`.

```bash
python app.py
```

> The server will typically run at:\
> 🔗 [http://0.0.0.0:5000](http://0.0.0.0:5000)\
> or the port set by your `PORT` environment variable.

---

### 2. Open the Frontend in Your Browser

Once the backend is running, navigate to:

```text
http://localhost:5000/
```

> (If deployed on a hosting platform like Render, use the public URL provided.)

---

## 💡 Usage

### 🔘 Register

1. Click **"✚ Register"**
2. Enter a unique username
3. Click **"✚ Generate Keys & Register"**

✅ An RSA key pair is generated on the server, and you're logged in for the session.

---

### 🔐 Login

1. Click **"🔒 Login"**
2. Enter your previously registered username
3. Click **"🔒 Login"**

✅ You're re-associated with your existing keys (in the server session).

---

### ✉️ Send Message

1. After logging in, the **"Send Message"** button appears
2. Click it and:
   - Enter the **receiver’s username**
   - Enter your **message**
3. Your message is encrypted with the receiver's public key and sent

---

### 📥 Receive Message

- When a message is sent to you, an **alert** pops up in your browser with the **encrypted message**.

> ⚠️ Note: Decryption is currently handled on the **server side**. For full E2EE, decryption should occur **on the client** using the private key.

---

## ⚠️ Current Limitations

| Limitation                 | Description                                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------------- |
| 🔐 **Private Key Storage** | Private keys are stored in-memory on the server (`private_keys` dict). Not secure for production.        |
| 🧠 **No Persistent Data**  | All registrations & keys are in memory. Server restart = data loss. A real app needs a database.         |
| 🔓 **Basic Login Only**    | No passwords, sessions, JWTs or cookies. Just temporary server-side user association.                    |
| 🔍 **Server Decryption**   | Server holds private keys, meaning it can decrypt messages. Not true E2EE.                               |
| 🔐 **No AES Used Yet**     | Currently, only RSA is used. AES-256 with hybrid encryption (RSA for key, AES for message) is ideal.     |
| 📡 **Socket Rooms**        | Messages are emitted using `room=receiver`. For better control, manage Socket.IO session IDs explicitly. |

---

## 🤝 Contributing

Contributions are welcome!\
Got ideas, bug fixes, or features? Open an issue or submit a pull request.

---

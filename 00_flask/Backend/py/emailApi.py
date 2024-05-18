from flask import Flask, request, jsonify, redirect, url_for
from google.oauth2 import id_token
from google.auth.transport import requests
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Google OAuth 2.0 client ID obtained by registering your application
CLIENT_ID = '962871581155-optkb11uv3m80s4uj9kqc0if4eldc1g9.apps.googleusercontent.com'

# Email server configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

@app.route('/', methods=['POST'])
def send_email():
    # Get email and message from the request
    sender_email = request.form.get('email')
    message = request.form.get('message')

    if not sender_email or not message:
        return jsonify({'error': 'Email and message are required'}), 400

    # Verify OAuth 2.0 token
    token = request.headers.get('Authorization')
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        if id_info['email'] != sender_email:
            return jsonify({'error': 'Invalid email address'}), 401
    except Exception as e:
        return jsonify({'error': 'Failed to verify token'}), 401

    # Create email message
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Message from Flask API'
    msg['From'] = sender_email
    msg['To'] = 'levygesy123@gmail.com'  # Your email address as the recipient

    try:
        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(sender_email, None)  # No password needed for OAuth 2.0
            smtp.send_message(msg)
    except Exception as e:
        return jsonify({'error': 'Failed to send email'}), 500

    return jsonify({'message': 'Email sent successfully'}), 200

@app.route('/login')
def login():
    # Redirect users to Google's OAuth 2.0 authentication page
    return redirect('https://accounts.google.com/o/oauth2/auth?response_type=token&client_id=' + CLIENT_ID + '&redirect_uri=' + url_for('authorized', _external=True))

@app.route('/authorized')
def authorized():
    # Handle the OAuth 2.0 callback and obtain access token
    access_token = request.args.get('access_token')
    if access_token:
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'error': 'Access token not found'}), 400

if __name__ == '__main__':
    app.run(debug=True)

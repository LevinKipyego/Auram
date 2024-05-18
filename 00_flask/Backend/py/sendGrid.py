from flask import Flask, request, jsonify, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

SENDGRID_API_KEY = 'your-sendgrid-api-key'
SENDER_EMAIL = 'your-sender-email@example.com'

@app.route('/send_email', methods=['POST'])
def send_email():
    # Get email and message from the request
    recipient_email = request.form.get('email')
    message = request.form.get('message')

    if not recipient_email or not message:
        return jsonify({'error': 'Email and message are required'}), 400

    # Create a SendGrid message
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient_email,
        subject='Message From Client!',
        plain_text_content=message)

    try:
        # Send the email using the SendGrid API
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        return jsonify({'error': 'Failed to send email'}), 500

    return jsonify({'message': 'Email sent successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

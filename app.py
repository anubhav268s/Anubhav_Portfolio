from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Your Gmail credentials
EMAIL_ADDRESS = 'example@gmail.com'
EMAIL_PASSWORD = 'urwi rokb dfbm frkn'  # From Gmail app passwords

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if not all([name, email, subject, message]):
            return jsonify({'error': 'All fields are required'}), 400

        # Compose email
        email_message = EmailMessage()
        email_message['Subject'] = f"Contact Form: {subject}"
        email_message['From'] = EMAIL_ADDRESS
        email_message['To'] = EMAIL_ADDRESS  # Send to yourself
        email_message.set_content(
            f"New message from {name} ({email}):\n\n{message}"
        )

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(email_message)

        return jsonify({'status': 'success', 'message': 'Message sent to your email'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

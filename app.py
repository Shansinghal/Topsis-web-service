
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, render_template, request, jsonify
from topsis_logic import calculate_topsis
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# EMAIL CONFIGURATION - REPLACE WITH YOUR CREDENTIALS OR USE ENV VARS
# For Gmail, you need an App Password if 2FA is on.
EMAIL_ADDRESS = os.getenv('EMAIL_USER', 'your_email@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS', 'your_app_password')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    weights_str = request.form.get('weights')
    impacts_str = request.form.get('impacts')
    email_dest = request.form.get('email')

    if not all([weights_str, impacts_str, email_dest]):
         return jsonify({'error': 'Missing form data'}), 400

    try:
        # Parse weights and impacts
        weights = [float(w.strip()) for w in weights_str.split(',')]
        impacts = [i.strip() for i in impacts_str.split(',')]
    except ValueError:
        return jsonify({'error': 'Invalid weights format. Must be numbers separated by commas.'}), 400

    # Save file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Run TOPSIS
        output_file_path = calculate_topsis(file_path, weights, impacts)
        
        # Send Email
        send_email(email_dest, output_file_path)
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_email(to_email, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "TOPSIS Analysis Results"

    body = "Please find attached the results of your TOPSIS analysis."
    msg.attach(MIMEText(body, 'plain'))

    filename = os.path.basename(attachment_path)
    attachment = open(attachment_path, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Note: This might fail if invalid credentials are provided.
        # Ideally, we should handle this gracefully but for this assignment, we assume valid creds or user config.
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
    finally:
        attachment.close()

if __name__ == '__main__':
    app.run(debug=True)

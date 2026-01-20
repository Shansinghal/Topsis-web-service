import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from topsis_logic import calculate_topsis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes (useful if user does use Live Server, but we recommend python app.py)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Email Configuration
EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

@app.route('/')
def index():
    """Serves the main page."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handles file submission, TOPSIS calculation, and emailing results."""
    # 1. Validate File
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 2. Extract Data
    weights_str = request.form.get('weights')
    impacts_str = request.form.get('impacts')
    email_dest = request.form.get('email')

    if not all([weights_str, impacts_str, email_dest]):
         return jsonify({'error': 'Missing required form data (weights, impacts, or email)'}), 400

    try:
        # 3. Parse and Validate Inputs
        weights = [float(w.strip()) for w in weights_str.split(',')]
        impacts = [i.strip() for i in impacts_str.split(',')]
    except ValueError:
        return jsonify({'error': 'Invalid weights format. Must be numbers separated by commas.'}), 400

    # 4. Save Uploaded File
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # 5. Run TOPSIS Logic
        output_file_path = calculate_topsis(file_path, weights, impacts)
        
        # 6. Send Email
        send_email(email_dest, output_file_path)
        
        return jsonify({'success': True, 'message': 'Result sent to email successfully.'})
    
    except Exception as e:
        # Log the full error for debugging (visible in Render logs)
        print(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

def send_email(to_email, attachment_path):
    """Sends the result file via email."""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise Exception("Email credentials not configured on server.")

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "TOPSIS Analysis Results"

    body = "Please find attached the results of your TOPSIS analysis."
    msg.attach(MIMEText(body, 'plain'))

    filename = os.path.basename(attachment_path)
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)
    
    try:
        # standard 30s timeout for connection
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        raise Exception(f"SMTP Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

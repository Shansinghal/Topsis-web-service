# TOPSIS Analysis Web Service

![TOPSIS Analysis](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)

A comprehensive web-based tool to perform TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) analysis. This application allows users to rank alternatives based on multiple criteria by uploading a dataset, defining weights, and specifying impacts.

🚀 **Live Demo:** [https://topsis-web-service-vzxs.onrender.com/](https://topsis-web-service-vzxs.onrender.com/)

## 📋 Features

- **User-Friendly Interface**: Clean, modern, and responsive card-based design.
- **Dynamic Analysis**: Works with any dataset (CSV/Excel) containing numeric criteria.
- **Instant Validation**: Real-time frontend validation for file types, weights, and impacts.
- **Email Integration**: Automatically sends the detailed result file (with TOPSIS Score and Rank) to your email.
- **Secure**: Uses environment variables for sensitive credentials.

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Backend**: Python (Flask)
- **Data Processing**: Pandas, NumPy
- **Email Service**: SMTP (Gmail)

## 📂 Project Structure

```
├── app.py              # Main Flask application
├── topsis_logic.py     # Core Algorithm Implementation
├── requirements.txt    # Python dependencies
├── Procfile            # Deployment configuration (Render/Heroku)
├── .env                # Environment variables (Email Credentials)
├── templates/
│   └── index.html      # Frontend HTML
├── static/
│   ├── style.css       # Custom Styling
│   └── script.js       # Client-side Logic
└── outputs/            # Directory for generated result files
```

## 🚀 How to Run Locally

### Prerequisites
- Python 3.x installed
- Gmail App Password (for email functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/topsis-web-service.git
   cd topsis-web-service
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory (or rename the example):
   ```ini
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

## 📝 Usage Guide

1. **Upload File**: Select a `.csv` or `.xlsx` file containing your data.
   - *Note: The file must contain a header row. Non-numeric columns are ignored during calculation.*
2. **Weights**: Enter weights for each numeric criterion separated by commas (e.g., `0.25,0.25,0.25,0.25`).
3. **Impacts**: Enter impacts as `+` (positive/benefit) or `-` (negative/cost) separated by commas (e.g., `+,+,-,+`).
4. **Email**: Enter the email address where you want to receive the report.
5. **Submit**: Click submit and wait for the "Success" message. Check your inbox for the results!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

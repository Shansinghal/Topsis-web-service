import streamlit as st
import pandas as pd
import numpy as np
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from topsis_logic import calculate_topsis_score
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="TOPSIS Analysis", page_icon="📊")

st.title("📊 TOPSIS Analysis Web Service")
st.write("Upload your data, define weights and impacts, and get the ranked results.")

# Sidebar for email configuration (optional/hidden or minimal)
# or just inline
st.markdown("---")

# File Upload
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

# Form inputs
col1, col2 = st.columns(2)
with col1:
    weights_input = st.text_input("Weights (comma separated)", placeholder="1,1,1,1")
with col2:
    impacts_input = st.text_input("Impacts (comma separated, + or -)", placeholder="+,+,-, +")

email_input = st.text_input("Email (optional, to receive results)", placeholder="user@example.com")

def send_email_streamlit(to_email, df_result):
    """Sends the result dataframe as CSV via email."""
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')
    
    if not email_user or not email_pass:
        st.error("Email credentials not configured on server.")
        return False

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = "TOPSIS Analysis Results (Streamlit)"

    body = "Please find attached the results of your TOPSIS analysis."
    msg.attach(MIMEText(body, 'plain'))

    # Convert DF to CSV string
    csv_content = df_result.to_csv(index=False)
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_content)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="topsis_result.csv"')
    msg.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"SMTP Error: {str(e)}")
        return False

if st.button("Calculate TOPSIS"):
    if uploaded_file is not None:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Validation
            if not weights_input or not impacts_input:
                st.error("Please provide weights and impacts.")
            else:
                weights = [float(w.strip()) for w in weights_input.split(',')]
                impacts = [i.strip() for i in impacts_input.split(',')]
                
                # Calculate
                result_df = calculate_topsis_score(df, weights, impacts)
                
                # Show results
                st.success("Calculation Successful!")
                st.dataframe(result_df)
                
                # Download button
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Result as CSV",
                    data=csv,
                    file_name='topsis_result.csv',
                    mime='text/csv',
                )
                
                # Send Email if provided
                if email_input:
                    with st.spinner('Sending email...'):
                        if send_email_streamlit(email_input, result_df):
                            st.success(f"Results sent to {email_input}")
                            
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file to start.")

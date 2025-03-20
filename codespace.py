from flask import Flask
import os
import subprocess
from datetime import datetime
import pytz

# Initialize Flask app
app = Flask(__name__)

# Define the /htop route
@app.route('/htop')
def show_htop():
    # Personal Details
    full_name = "Your Full Name Here"  # Replace with your actual full name
    
    # Retrieve system username
    try:
        user_name = os.getlogin()
    except OSError:
        # Fallback if os.getlogin() fails
        user_name = os.environ.get('USER') or os.environ.get('USERNAME') or 'Unknown'
    
    # Get server time in IST
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_timezone).strftime("%Y-%m-%d %H:%M:%S")
    
    # Capture output of 'top' command
    try:
        top_data = subprocess.check_output(["top", "-b", "-n", "1"], universal_newlines=True)
        top_lines = "\n".join(top_data.splitlines()[:20])  # Limit to first 20 lines
    except Exception as e:
        top_lines = f"Error retrieving top data: {e}"
    
   
    html_output = f"""
    <html>
        <head><title>System Monitor</title></head>
        <body>
            <h2>Name: {full_name}</h2>
            <h3>Username: {user_name}</h3>
            <h3>Server Time (IST): {current_time}</h3>
            <pre>{top_lines}</pre>
        </body>
    </html>
    """
    return html_output

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


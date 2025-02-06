from flask import Flask, render_template, request, jsonify
import pygsheets
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

gc = pygsheets.authorize(service_file='google_credentials.json')
spreadsheet = gc.open('autocount')

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
MANAGER_EMAIL = os.getenv("MANAGER_EMAIL")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    data = {}
    for worksheet in spreadsheet.worksheets():
        van_name = worksheet.title
        sheet_data = worksheet.get_all_values()
        sheet_data = [list(filter(lambda x: x.strip(), row)) for row in sheet_data]
        headers = sheet_data[0]
        rows = [row for row in sheet_data[1:] if any(cell.strip() for cell in row)]
        data[van_name] = {"headers": headers, "rows": rows}
    return jsonify(data)

@app.route('/check_discrepancies', methods=['POST'])
def check_discrepancies():
    mismatches = []
    for worksheet in spreadsheet.worksheets():
        van_name = worksheet.title
        data = worksheet.get_all_values()
        for i in range(1, len(data)):
            part_number = data[i][0]
            part_description = data[i][1]
            scale_count = data[i][2]
            technician_count = data[i][3]

            try:
                scale_count = int(scale_count)
                technician_count = int(technician_count)
            except ValueError:
                continue  
            
            if scale_count != technician_count:
                highlight_row(worksheet, i + 1)
                mismatches.append({
                    "van_name": van_name,
                    "part_number": part_number,
                    "description": part_description,
                    "scale_count": scale_count,
                    "technician_count": technician_count
                })
                send_email(van_name, part_number, part_description, scale_count, technician_count)
    
    return jsonify({"mismatches": mismatches})

def highlight_row(worksheet, row):
    cell_range = f"A{row}:D{row}"
    cells = worksheet.range(cell_range, returnas='cells')
    flat_cells = [cell for cell_row in cells for cell in cell_row]
    for cell in flat_cells:
        cell.color = (1, 0, 0)
    worksheet.update_cells(flat_cells)

def send_email(van_name, part_number, part_description, scale_count, technician_count):
    subject = f"Inventory Discrepancy in {van_name}: Part {part_number}"
    body = f"""
    Discrepancy Found in Weekly Inventory Check for **{van_name}**:

    - Part Number: {part_number}
    - Description: {part_description}
    - Scale Count: {scale_count}
    - Technician Count: {technician_count}

    Please review this discrepancy.
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = MANAGER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, MANAGER_EMAIL, msg.as_string())
        server.quit()
        print(f"Email sent for part {part_number} in {van_name}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
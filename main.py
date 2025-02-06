import pygsheets
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

# Google Sheets Authentication
gc = pygsheets.authorize(service_file='google_credentials.json')
spreadsheet = gc.open('autocount')  

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
MANAGER_EMAIL = os.getenv("MANAGER_EMAIL")


def compare_counts():
    #Iterates through all vans on the sheet and checks for inventory discrepancies
    for worksheet in spreadsheet.worksheets(): 
        van_name = worksheet.title 
        data = worksheet.get_all_values()

        for i in range(1, len(data)):  
            part_number = data[i][0]
            part_description = data[i][1]
            scale_count = data[i][2]
            technician_count = data[i][3]

            # Make sure we are comparing only integers
            try:
                scale_count = int(scale_count)
                technician_count = int(technician_count)

            # Skip a row if it has an invalid value
            except ValueError:
                continue  
            
            if scale_count != technician_count:
                highlight_row(worksheet, i + 1)
                send_email(van_name, part_number, part_description, scale_count, technician_count)

#Function to highlight rows with discrepencies
def highlight_row(worksheet, row):
    # Highlights a row in red if there's a mismatch
    cell_range = f"A{row}:D{row}"  
    cells = worksheet.range(cell_range, returnas='cells') 

    flat_cells = [cell for cell_row in cells for cell in cell_row]


    for cell in flat_cells:
        cell.color = (1, 0, 0) 

    worksheet.update_cells(flat_cells) 

def send_email(van_name, part_number, part_description, scale_count, technician_count):
    # Sends an email to the manager for discrepancies, including the van name
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

if __name__ == "__main__":
    compare_counts()

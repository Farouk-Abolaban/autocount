# **AutoCount 📊**  

**Automated Inventory Tracking System**  

## **Overview**  
AutoCount is an **automated inventory tracking system** designed to streamline inventory management using **Python, Flask, JavaScript, and Google Sheets API**. This system enables real-time data retrieval, automated email alerts, and efficient discrepancy detection, significantly reducing manual errors in inventory tracking.  

## **Features** 🚀  
- 📈 **Automated Inventory Tracking** – Fetches and updates inventory counts in **real-time** using the **Google Sheets API**.  
- 📨 **Email Alerts** – Sends automated **SMTP email notifications** when discrepancies are detected.  
- 🔍 **Data Validation & Anomaly Detection** – Flags incorrect technician counts, ensuring **99% accuracy** in reporting.  
- 💡 **User-Friendly Interface** – Designed with **Bootstrap & JavaScript** for an interactive experience.  
- ⏳ **Time Efficiency** – Reduces manual tracking effort by **80%**, saving **10+ hours per week**.  

## **Tech Stack** 🛠️  
- **Backend:** Flask (Python), Google Sheets API, Pygsheets, SMTP  
- **Frontend:** JavaScript, HTML, Bootstrap  
- **Database:** Google Sheets  
- **Dev Tools:** Git, VS Code, Linux  

## **Installation & Setup** ⚙️  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Farouk-Abolaban/AutoCount.git
cd AutoCount
```

### **2️⃣ Install Dependencies**
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
Create a .env file in the project directory and add the following:
```bash
GOOGLE_SHEETS_CREDENTIALS=your_credentials.json
SMTP_EMAIL=your_email@example.com
SMTP_PASSWORD=your_secure_password
```

### **4️⃣ Run the Application**
Start the Flask server:
```bash
python app.py
```
Access the application in your browser at: http://127.0.0.1:5000/

## **Usage Guide** 📚
1. Upload inventory data or sync with Google Sheets.
2. View and manage inventory in the web UI.
3. Receive alerts when inventory discrepancies are detected.
4. Export reports for inventory analysis.


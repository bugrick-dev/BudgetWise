# 💰 BudgetWise
A simple **personal finance tracker** built with Flask, SQLite, and Chart.js.  
BudgetWise helps you **log transactions, categorize expenses, visualize spending trends**, and set savings goals.  

---

## 🚀 Features
- 🔐 User authentication (register/login/logout with hashed passwords)  
- ➕ Add manual transactions (amount, category, description, date)  
- 📂 Upload CSV bank statements for quick imports  
- 🏷️ Auto-categorization suggestions based on keywords  
- 📊 Interactive dashboard with **Chart.js**:
  - Pie chart of spending by category  
  - Line chart of expenses over time  
- 🎯 Optional: savings goals tracking  

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask  
- **Database:** SQLite  
- **Frontend:** HTML, Bootstrap, Chart.js  
- **Extras:** Pandas/CSV for file parsing, Werkzeug for password hashing  

---

## 📂 Project Structure
budgetwise/  
│── app.py # Flask app  
│── helpers.py # Utility functions (auth, db, etc.)  
│── requirements.txt # Dependencies  
│── budgetwise.db # SQLite database  
│── templates/ # HTML templates (Jinja2)  
│ ├── layout.html  
│ ├── index.html # Dashboard  
│ ├── login.html  
│ ├── register.html  
│ ├── add_transaction.html  
│ └── upload_csv.html  
│── static/ # CSS, JS, images  
│ ├── styles.css  
│ └── charts.js  

---

## ⚡ Installation & Setup  
1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/budgetwise.git
   cd budgetwise
2. **Create a virtual environment**  
    ```bash
    python -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate      # Windows 
    export FLASK_APP=app.py # Set environment variables
    ```
3. **Install dependencies**  
    ```bash
    pip install -r requirements.txt
    ```
4. **Initialize database**  
    ```bash
        flask shell
    >>> from app import init_db
    >>> init_db()
    >>> exit()
    ```
5. **Run Server**  
    ```bash
    flask run
    ```
6. **Open in your browser** 
    ```
    http://127.0.0.1:5000
    ``` 
## 🔐 Security Notes  
Passwords are stored securely using `werkzeug.security.generate_password_hash`.  
**Never** store raw passwords in the database.
## 📊 Example Dashboard
**Pie Chart:** Spending distribution across categories  
**Line Chart:** Monthly spending trend  
(screenshot placeholder — add your own)
## 📝 Future Improvements
🔄 Currency conversion API integration  
📱 Mobile-friendly dashboard view  
📊 Export reports as PDF/CSV  
👥 Shared accounts for group budgeting  



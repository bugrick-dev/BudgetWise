# 💰 BudgetWise
A simple **personal finance tracker** built with Flask, SQLite, and Chart.js.  
BudgetWise helps you **log transactions, categorize expenses, visualize spending trends**, and set savings goals.  

![Welcome Page](screenshots/welcome.png)

---

## 🚀 Features
- 🔐 User authentication (register/login/logout with hashed passwords)  
- 🌑 Dark mode and 🌕 Light mode support
- ➕ Add manual transactions (amount, category, description, date)    
- 📊 Interactive dashboard with **Chart.js**:
  - Pie chart of spending by category  
  - Line chart of expenses over time
    

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask  
- **Database:** SQLite, SQLAlchemy  
- **Frontend:** HTML, Bulma, Chart.js  
- **Extras:**  Werkzeug for password hashing  

---

## 📂 Project Structure
budgetwise/  
│── app.py # Flask app  
│── helpers.py # Utility functions  
│── requirements.txt # Dependencies    
│── screenshots/ # Screenshots    
│── templates/ # HTML templates (Jinja2)    
└── static/ # CSS, images  
  

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
    flask init-db
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

![Dashboard View](screenshots/dashboard.png)

## 📝 Future Improvements
🔄 Currency conversion API integration  
📱 Mobile-friendly dashboard view  
📊 Export reports as PDF/CSV  
👥 Shared accounts for group budgeting  
📱Will come to mobile devices!

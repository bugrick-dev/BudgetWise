# 💰 BudgetWise
BudgetWise is a lightweight yet powerful **personal finance tracker** designed to help individuals take control of their money with minimal effort. Built using **Flask, SQLite, and Chart.js**, this project demonstrates how simple tools and technologies can combine to create a polished and useful application.  

Whether you want to keep an eye on daily spending, monitor monthly expenses, or gain insight into long-term financial trends, BudgetWise provides a clear and intuitive interface to help you make smarter money decisions.  

With **user authentication, expense categorization, and interactive data visualizations**, BudgetWise makes personal finance tracking straightforward for anyone, from beginners to more advanced users.  

---

## 🎥 Video Demo  
See BudgetWise in action here: **[YouTube Demo](https://youtu.be/QaGPdCwhGLs)**  

![Welcome Page](screenshots/welcome.png)

---

## 🚀 Features
BudgetWise comes with a solid set of features that make financial tracking both functional and enjoyable:  

- 🔐 **User Authentication**  
  - Secure registration and login system with password hashing.  
  - Session-based authentication ensures user data is private and accessible only when logged in.  

- 🌗 **Dark Mode / Light Mode Support**  
  - Switch between dark and light themes to match your preference.  
  - Provides a modern and accessible user experience.  

- ➕ **Add Transactions**  
  - Record income or expenses with details like **amount, category, description, and date**.  
  - Categories make it easy to separate essentials (like groceries, rent) from discretionary spending (like dining out, entertainment).  

- 📊 **Interactive Dashboard** powered by Chart.js  
  - **Pie Chart**: Displays spending distribution across categories.  
  - **Line Chart**: Shows expense trends over time for long-term insights.  
  - Charts are dynamic and update automatically as you log new transactions.  

These features combine to provide a simple but effective budgeting solution that can be run locally or extended further for personal or professional use.  

---

## 🛠️ Tech Stack
BudgetWise leverages a proven and lightweight tech stack:  

- **Backend:** [Flask](https://flask.palletsprojects.com/) – A micro web framework for Python. Handles routes, authentication, and business logic.  
- **Database:** [SQLite](https://www.sqlite.org/) with SQLAlchemy ORM – Stores users and transactions in a lightweight relational database.  
- **Frontend:** HTML templates styled with [Bulma](https://bulma.io/), a modern CSS framework, along with interactive charts via [Chart.js](https://www.chartjs.org/).  
- **Security:** Password hashing with Werkzeug to keep user data safe.  

This tech stack makes BudgetWise easy to deploy, maintain, and extend while keeping performance and security in mind.  

---

## 📂 Project Structure
Here’s an overview of the folder structure:  

```
budgetwise/  
│── app.py             # Main Flask app entry point  
│── helpers.py         # Utility functions (e.g., database setup, auth helpers)  
│── requirements.txt   # Python dependencies    
│── screenshots/       # Screenshots used in README    
│── templates/         # Jinja2 HTML templates    
└── static/            # Static files (CSS, images, JS)  
```

This modular layout keeps the project organized and makes it easier to add new features later.  

---

## ⚡ Installation & Setup  
Follow these steps to get BudgetWise running on your local machine:  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/budgetwise.git
   cd budgetwise
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows 
   ```

   Export environment variables (if needed):  
   ```bash
   export FLASK_APP=app.py
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**  
   ```bash
   flask init-db
   ```

5. **Run the Flask development server**  
   ```bash
   flask run
   ```

6. **Open in your browser**  
   Navigate to:  
   ```
   http://127.0.0.1:5000
   ```  

Once set up, you can register as a new user, log in, and start tracking your finances immediately.  

---

## 🔐 Security Notes  
BudgetWise takes security seriously:  

- Passwords are **never stored in plain text**. Instead, they are hashed using `werkzeug.security.generate_password_hash`.  
- Authentication uses session-based cookies, keeping users logged in securely without exposing sensitive data.  
- Since this is a demo project, additional layers such as HTTPS, CSRF protection, and production-ready deployment settings are recommended if used beyond a local environment.  

---

## 📊 Example Dashboard
The dashboard is the heart of BudgetWise, giving users a clear view of their financial habits.  

- **Pie Chart:** Visualizes the proportion of spending in different categories (e.g., rent, food, transport).  
- **Line Chart:** Highlights monthly or weekly spending patterns over time, making it easier to spot trends or sudden spikes in expenses.  

![Dashboard View](screenshots/dashboard.png)

These visualizations make raw data more meaningful and encourage better financial decision-making.  

---

## 📝 Future Improvements
BudgetWise is a starting point, and many exciting features could be added to make it even more powerful:  

- 🔄 **Currency Conversion API** – Automatically convert transactions into different currencies.  
- 📱 **Responsive Dashboard** – Improve mobile usability for on-the-go budgeting.  
- 📊 **Export Reports** – Download expense summaries in PDF or CSV format for archiving or tax purposes.  
- 👥 **Shared Accounts** – Enable family members or roommates to track expenses together.  
- 📱 **Mobile App Integration** – Extend BudgetWise to iOS/Android for native mobile experiences.  

These ideas offer plenty of opportunities for contributions and enhancements.  

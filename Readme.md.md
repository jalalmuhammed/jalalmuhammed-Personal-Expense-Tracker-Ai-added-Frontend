
# 💰 Personal Expense Tracker (AI-Enhanced Frontend)

A smart and efficient **Personal Expense Tracker** designed to help users record, manage, and analyze their daily expenses. This project includes a powerful backend built in **Python** and an AI-generated, visually engaging **frontend** to enhance usability and analytics.

---

## 📦 Project Overview

This project was originally built as a **command-line-based** expense tracker with powerful features like:

- Expense addition, editing, deletion
- Filtering by category and date
- Monthly and category-wise summaries
- CSV export functionality

To improve usability and interface design, the **frontend has been added using AI tools**, transforming it into a full-fledged web-based dashboard.

> 🧠 **Note:** The entire backend was developed manually. The frontend was generated using AI design tools.

---

## ✨ Features

### Backend (Python + Flask)

- API to handle CRUD operations on expenses
- Filter, summarize, and export data
- Data validation and storage using JSON files
- Flask-powered RESTful API

### Frontend (AI-Generated UI)

- Responsive, modern dashboard with Chart.js for visual insights
- Interactive sections for:
  - Dashboard Overview
  - Add Expense
  - View Expenses
  - Analytics
  - Filters
- Modal-based editing interface
- AI-generated layout with clean UI/UX principles

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/expense-tracker-ai-frontend.git
cd expense-tracker-ai-frontend
```

### 2. Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

> **Note:** Ensure `Flask` and `Flask-CORS` are installed.

### 3. Run the Backend

```bash
python app.py
```

Server will start at `http://localhost:5000`

### 4. Open the Frontend

Open `index.html` in your browser or navigate to `http://localhost:5000` after running the backend.

---

## 📂 Project Structure

```bash
.
├── app.py               # Flask API server
├── main.py              # CLI-based version (Legacy)
├── index.html           # AI-generated frontend
├── data_manager.py      # Handles data load/save operations
├── reporter.py          # Summarization and filtering logic
├── utils.py             # Validation and helper methods
├── constants.py         # Constants and config paths
└── data/
    └── Expenses.json    # Stores all expenses
```

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (AI-designed)
- **Visualization:** Chart.js
- **Data Storage:** JSON

---

## 🙌 Acknowledgement

- Backend fully handcrafted by [Your Name]
- Frontend designed and enhanced using **AI tools** to demonstrate the integration of AI-assisted UI generation with developer-built logic

---

## 📬 Contact

For questions or collaboration:
- 📧 your-email@example.com
- 🌐 [LinkedIn](https://linkedin.com/in/your-profile)

---

> 🔥 This project is a fusion of human logic and AI design. Built to track money, powered by intelligence.

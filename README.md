#  AI Financial Data Analyzer

## 📌 Overview

AI Financial Data Analyzer is a FastAPI-based application that extracts, processes, and analyzes financial data using intelligent services. It provides structured insights, logging, and efficient data handling for financial datasets.

---

##  Features

* 📊 Financial data extraction and processing
* 🤖 AI-powered analysis
* 🗂️ Structured API endpoints
* 📁 Logging system (success & error logs)
* 💾 Database integration (SQLite)
* 📈 CSV and JSON data handling

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **Database:** SQLite
* **Libraries:** Pydantic, Uvicorn
* **Others:** Logging, CSV handling

---

## 📂 Project Structure

```
app/
 ├── core/          # Config, database, security
 ├── models/        # Database models & schemas
 ├── routes/        # API routes
 ├── services/      # AI & business logic
 ├── utils/         # Helper functions
 └── main.py        # Entry point

data/               # Database & datasets
logs/               # Log files
requirements.txt    # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/AI-Financial-Data-Analyzer.git
cd AI-Financial-Data-Analyzer
```

### 2️⃣ Create virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
uvicorn app.main:app --reload
```

👉 Open in browser:

```
http://127.0.0.1:8000
```

👉 API Docs:

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Functionality

* Extract financial data
* Process and analyze data
* Store results in database
* Generate logs and metrics

---

## 🔒 Security Note

* `.env` file is ignored using `.gitignore`
* Sensitive data is not uploaded to GitHub

---

## 🎓 Use Cases

* Financial data analysis
* Backend API development practice
* AI-based data processing projects

---

## 👨‍💻 Author

**Yug Vahanka**

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!

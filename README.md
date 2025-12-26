# Meqenete – Personal Finance Tracker API

Meqenete is a RESTful backend API built with Django and Django REST Framework for tracking personal income, expenses, and monthly financial summaries.

This project was developed as a backend capstone project with a focus on authentication, filtering, pagination, and production deployment.

---

## Features

- User registration and JWT authentication
- Expense and income management (CRUD)
- Category-based expense tracking
- Monthly financial summary
- Filtering by category, month, and year
- Pagination support
- PostgreSQL database
- Production-ready deployment

---
  
## Tech Stack

- Python
- Django & Django REST Framework
- PostgreSQL
- Simple JWT
- django-filter
- Railway (deployment)

---

## Project Structure

```
alx_capstone/
├── README.md                 # Project documentation
├── Finance_tracker/          # Django project folder
│   ├── manage.py             # Django management commands
│   ├── Finance_tracker/      # Project-level settings
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py           # Project-level URLs
│   │   └── wsgi.py           # WSGI configuration
│   └── meqenete/             # App for Meqenete functionality
│       ├── models.py         # Models for income, expenses, etc.
│       ├── views.py          # API views
│       ├── serializers.py    # Serializers for API endpoints
|       └── urls.py           # App-level URLS 
├── requirements.txt          # Project dependencies
├── Procfile                  # Deployment configuration for Railway/Heroku
└── build.sh                  # Deployment build script
```
---

## Setup Instructions
### 1️⃣ Clone the repository:
```bash
git clone https://github.com/SumeyaMuhammed/ALX_Capstone_Project
cd ALX_Capstone_Project/Finance_tracker
```

### 2️⃣ Create and activate virtual environment
- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

- Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables
To run this project locally, you will need to create a `.env` file in the root of your project directory. This file should contain the following environment variables:
```env
DB_HOST=localhost
DB_NAME=meqenete
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

SECRET_KEY=your-secret-key
DEBUG=False
```

### 5️⃣ Run database migrations
```bash
python manage.py migrate
```

### 6️⃣ Start the development server
```bash
python manage.py runserver
```
---

## API Overview
### Authentication
- **Register User**  
  ```http
  POST /api/auth/register/
  ```

- **Login User (JWT)**  
  ```http
  POST /api/auth/login/
  ```

### Expenses
- **List Expenses**  
  ```http
  GET /api/expenses/
  ```

- **Create Expense**  
  ```http
  POST /api/expenses/
  ```

- **Filtering Example**
   ```http
   GET /api/expenses/?category_name=Food&month=12&year=2025
   ```

### Income
- **List Income**  
  ```http
  GET /api/income/
  ```

- **Create Income**  
  ```http
  POST /api/income/
  ```

### Monthly Summary
```http
GET /api/summary/?month=12&year=2025
```

---

## Deployment
The API is deployed on Railway using:
- gunicorn as the WSGI server
- PostgreSQL database
- dj_database_url for environment-based configuration


## Author
**Sumeya Muhammed**

Backend Software Engineering Student

ALX Backend Web Development Program

## License
This project is intended for educational purposes.
 

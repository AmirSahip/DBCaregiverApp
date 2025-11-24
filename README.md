# Caregiver Platform - Web Application

A Flask-based web application for managing the Caregiver Platform database with full CRUD (Create, Read, Update, Delete) operations.

## Features

- **User Management**: Create, read, update, and delete user accounts
- **Caregiver Management**: Manage caregiver profiles with hourly rates and caregiving types
- **Member Management**: Manage member profiles with house rules and dependent descriptions
- **Job Management**: Create and manage job postings

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Update database connection in `app.py`:
```python
connection_string = "postgresql://username:password@host:port/database"
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment on PythonAnywhere

1. **Create a PythonAnywhere account** (free tier available)

2. **Upload your files**:
   - Upload `app.py` to your home directory
   - Upload the `templates` folder
   - Upload `requirements.txt`

3. **Set up a web app**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask and Python 3.10
   - Set the path to your `app.py` file

4. **Install dependencies**:
   - Open a Bash console
   - Run: `pip3.10 install --user -r requirements.txt`

5. **Configure database**:
   - Update the connection string in `app.py` to use your PostgreSQL database
   - For PythonAnywhere, you may need to use their database or an external PostgreSQL service

6. **Reload the web app**:
   - Go to "Web" tab
   - Click "Reload" button

## Deployment on Heroku

1. **Install Heroku CLI** and login

2. **Create a Procfile**:
```
web: gunicorn app:app
```

3. **Update requirements.txt** to include gunicorn:
```
Flask==3.0.0
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

4. **Create Heroku app**:
```bash
heroku create your-app-name
```

5. **Set up PostgreSQL addon**:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

6. **Update connection string** in `app.py` to use environment variable:
```python
import os
connection_string = os.environ.get('DATABASE_URL', 'postgresql://...')
```

7. **Deploy**:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

## Project Structure

```
DB_ASSIGNMENT_3/
├── app.py                 # Main Flask application
├── queries.py             # SQL queries (Part 2)
├── database.sql           # Database schema (Part 1)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/            # HTML templates
    ├── base.html
    ├── index.html
    ├── users/
    ├── caregivers/
    ├── members/
    └── jobs/
```

## Notes

- Make sure your PostgreSQL database is accessible from your deployment platform
- Update the connection string with your actual database credentials
- For production, use environment variables for sensitive information like database passwords


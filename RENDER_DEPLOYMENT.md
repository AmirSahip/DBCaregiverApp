# Deploying to Render

## Step-by-Step Deployment Guide

### Prerequisites
1. Create a GitHub account (if you don't have one)
2. Create a Render account at https://render.com (free tier available)

### Step 1: Prepare Your Code

Your code is already prepared with:
- ✅ `Procfile` - tells Render how to run your app
- ✅ `requirements.txt` - includes gunicorn
- ✅ Environment variable support in `app.py`

### Step 2: Push to GitHub

1. **Initialize Git repository** (if not already done):
```powershell
cd "C:\Users\amirs\OneDrive\Рабочий стол\DB_ASSIGNMENT_3"
git init
git add .
git commit -m "Initial commit for Render deployment"
```

2. **Create a GitHub repository**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `caregiver-platform`)
   - **Don't** initialize with README

3. **Push your code to GitHub**:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/caregiver-platform.git
git branch -M main
git push -u origin main
```

### Step 3: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `caregiver-platform-db`
   - **Database**: `caregiver_platform`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **Plan**: Free (or paid if needed)
4. Click **"Create Database"**
5. **Important**: Copy the **Internal Database URL** (you'll need this later)

### Step 4: Deploy Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `caregiver-platform` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or paid)

4. **Add Environment Variables**:
   - Click **"Environment"** tab
   - Add:
     - **Key**: `DATABASE_URL`
     - **Value**: Paste the **Internal Database URL** from your PostgreSQL service
     - **Key**: `SECRET_KEY`
     - **Value**: Generate a random secret key (e.g., use: `python -c "import secrets; print(secrets.token_hex(32))"`)

5. Click **"Create Web Service"**

### Step 5: Initialize Database

After deployment, you need to run your `queries.py` to create tables and insert data:

1. **Option A: Using Render Shell** (Recommended)
   - Go to your Web Service in Render dashboard
   - Click **"Shell"** tab
   - Run: `python queries.py`
   - (Note: Update `queries.py` connection string to use `DATABASE_URL` environment variable)

2. **Option B: Update queries.py to use environment variable**:
   ```python
   import os
   connection_string = os.environ.get('DATABASE_URL', 'postgresql://postgres:123456@localhost:5432/caregiver_platform')
   if connection_string.startswith('postgres://'):
       connection_string = connection_string.replace('postgres://', 'postgresql://', 1)
   ```

### Step 6: Access Your Application

- Your app will be available at: `https://your-app-name.onrender.com`
- Render provides a free `.onrender.com` subdomain
- First deployment may take 5-10 minutes

## Important Notes

1. **Free Tier Limitations**:
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds
   - 750 hours/month free

2. **Database Connection**:
   - Use **Internal Database URL** for connection from your web service
   - This ensures secure connection within Render's network

3. **Environment Variables**:
   - Never commit secrets to GitHub
   - Always use environment variables for sensitive data

4. **Updates**:
   - Push to GitHub → Render auto-deploys
   - Each deployment takes 2-5 minutes

## Troubleshooting

- **Database connection errors**: Check DATABASE_URL environment variable
- **Build fails**: Check requirements.txt and build logs
- **App crashes**: Check logs in Render dashboard
- **Tables not found**: Run queries.py to initialize database

## Alternative: Manual Database Setup

If you prefer, you can:
1. Connect to Render PostgreSQL using a database client
2. Run your `database.sql` file directly
3. Or use Render's PostgreSQL web interface


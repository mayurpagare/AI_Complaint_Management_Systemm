# AI Complaint Management System

A complete Flask, SQLite, SQLAlchemy, HTML5, CSS3, and vanilla JavaScript web application for citizen complaint reporting and administrator complaint management. The app classifies complaints with local Python keyword matching, assigns priority automatically, supports image uploads, and provides admin analytics with canvas charts.

## 1. Software Prerequisites

- Python 3.12+
- Visual Studio Code
- Git
- Google Chrome
- SQLite, included with Python

No paid software, Docker, Node.js, or external AI API is required.

## 2. Installation Steps

```bash
git clone <your-repository-url>
cd AI_Complaint_Management_System
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## 3. Commands to Run

Start the application:

```bash
python app.py
```

Open Google Chrome and visit:

```text
http://127.0.0.1:5000
```

Production start command for hosting platforms:

```bash
gunicorn app:app
```

Default administrator account:

```text
Email: admin@complaints.local
Password: Admin@12345
```

You can override the default administrator values before first run:

Windows PowerShell:

```powershell
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="StrongPassword123"
python app.py
```

Linux/Mac:

```bash
ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=StrongPassword123 python app.py
```

## 4. Project Structure

```text
AI_Complaint_Management_System/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── database.db
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   ├── js/
│   │   ├── app.js
│   │   └── dashboard.js
│   ├── images/
│   └── uploads/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── complaint.html
│   ├── profile.html
│   ├── admin_dashboard.html
│   ├── complaints.html
│   ├── analytics.html
│   ├── 404.html
│   └── 500.html
├── models/
│   ├── user.py
│   └── complaint.py
├── routes/
│   ├── auth.py
│   ├── complaint.py
│   └── admin.py
├── utils/
│   ├── classifier.py
│   └── helper.py
└── instance/
    └── database.db
```

Key folders:

- `models/`: SQLAlchemy ORM models for users, admins, and complaints.
- `routes/`: Flask Blueprints for authentication, citizen complaints, and admin tools.
- `utils/`: Form helpers, upload validation, and keyword classifier logic.
- `templates/`: Jinja2 pages for the landing page, dashboards, forms, analytics, and errors.
- `static/css/`: Glassmorphism SaaS styling, responsive layout, dark mode, and dashboard styles.
- `static/js/`: Vanilla JavaScript for theme switching, navigation, ripples, validation, and charts.
- `static/uploads/`: Validated JPG/JPEG/PNG complaint evidence uploads.
- `instance/database.db`: Main SQLite database generated and migrated by SQLAlchemy on first run.

## 5. Troubleshooting

### `python` is not recognized

Install Python 3.12+ and ensure Python is added to PATH. On Windows, try:

```bash
py -3.12 -m venv venv
```

### Dependencies fail to install

Upgrade pip inside the virtual environment:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Port 5000 is already in use

Stop the other process or run Flask on a different port:

```bash
python -c "from app import app; app.run(port=5001, debug=True)"
```

### Admin login does not use new environment variables

The admin account is seeded only when the database is first created. Delete `instance/database.db` and rerun `python app.py` to reseed with new environment values.

### Uploaded images are rejected

Only `.jpg`, `.jpeg`, and `.png` files are allowed, and the maximum upload size is 4 MB.

### Charts do not appear

Use Google Chrome and ensure JavaScript is enabled. Charts use the built-in HTML5 canvas API and do not require external libraries.

## 6. Screenshots Placeholders

Landing Page:

```text
[Insert screenshot: modern hero section with Report Complaint CTA]
```

Citizen Dashboard:

```text
[Insert screenshot: citizen statistics and complaint history table]
```

Report Complaint Form:

```text
[Insert screenshot: complaint submission form with category auto-detect option]
```

Admin Dashboard:

```text
[Insert screenshot: admin statistics, charts, and recent complaints]
```

Manage Complaints:

```text
[Insert screenshot: search, filters, status update, delete, image view, and CSV export]
```

Analytics:

```text
[Insert screenshot: monthly, category, and priority distribution charts]
```

## Firebase Note

This Flask application is a server-rendered Python web app with SQLite. Firebase Hosting only serves static assets unless paired with a supported backend runtime or external service. Creating and uploading to a new Firebase project also requires an authenticated Google account session. The project is complete for local execution with the required command sequence, and it can be adapted later for a Firebase-compatible architecture if account access and hosting strategy are provided.

## Make the Website Live

The easiest way to make this project live like a normal website is Render.

### Deploy on Render

1. Create a GitHub repository.
2. Upload/push this `AI_Complaint_Management_System` folder to GitHub.
3. Create a free Render account at `https://render.com`.
4. Click `New +` and select `Web Service`.
5. Connect your GitHub repository.
6. Use these settings:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

7. Add environment variables:

```text
SECRET_KEY=choose-a-long-random-secret
ADMIN_EMAIL=admin@complaints.local
ADMIN_PASSWORD=Admin@12345
```

8. Click `Deploy Web Service`.
9. Render will generate a public URL such as:

```text
https://ai-complaint-management-system.onrender.com
```

### Important SQLite Note

SQLite is fine for demos and college projects. On some hosting providers, uploaded images and SQLite database changes may reset after redeploys. For a permanent production website, migrate the database to PostgreSQL and store uploads in cloud storage.

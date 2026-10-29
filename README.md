# TaxTrack — Tax Data Management and Automation System

A beginner-friendly portfolio project that demonstrates transaction management, input validation, SQL-backed storage, automatic sample tax calculations, monthly reporting, and CSV export.

> **Important:** This is a learning/demo application, not a tax filing, accounting, or compliance system. The user enters the sample tax rate. The app does not determine legally applicable tax rates. Use fictional data only.

## Features

- Dashboard with transaction count, total taxable amount, and calculated tax
- Add, view, search, edit, and delete transaction records (CRUD)
- SQLite database through SQLAlchemy (no separate database server needed to start)
- Server-side validation for required fields, negative amounts, and rate range
- Sample tax calculation using `amount × rate ÷ 100`
- Monthly summary report
- CSV export
- Responsive interface and monthly chart
- Automated tests with pytest

## Technology stack

- Python 3
- Flask
- Flask-SQLAlchemy / SQLite
- HTML, CSS, Jinja templates
- Chart.js for visualization
- pytest for tests

## Run locally (Windows)

1. Install Python 3.10 or newer.
2. Extract this repository ZIP and open the project folder in VS Code.
3. Open a terminal in the project folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt instead:

   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

6. Start the application:

   ```bash
   python app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is created automatically when the app starts. Keep `*.db` files out of GitHub; `.gitignore` already excludes them.

## Run tests

```bash
python -m pytest -v
```

## GitHub upload

1. Create a new empty repository on GitHub, for example `tax-data-management-system`.
2. Extract the ZIP.
3. In a terminal, navigate into the `tax_data_management_system` folder.
4. Run:

   ```bash
   git init
   git add .
   git commit -m "Build TaxTrack tax data management system"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/tax-data-management-system.git
   git push -u origin main
   ```

Replace `YOUR-USERNAME` with your GitHub username. If Git asks you to authenticate, follow GitHub's sign-in prompt.

## Suggested resume entry (after you run and verify it)

**Tax Data Management and Automation System**  
*Python, Flask, SQLAlchemy, SQLite, HTML, CSS, JavaScript, Chart.js*

- Built a web application to manage transaction records with create, search, update, and delete functionality.
- Implemented server-side input validation and automatic sample tax calculations.
- Developed monthly summary reports and CSV export for data analysis.
- Added dashboard metrics and monthly visualizations to summarize transaction data.

Only list features you have run and understand. This starter version uses SQLite, not MySQL, and does not currently include Power BI, authentication, or production deployment.

## Project structure

```text
tax_data_management_system/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── transaction_form.html
│   └── monthly_report.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## Learning extensions

- Replace SQLite with MySQL after understanding SQLAlchemy configuration.
- Add login/authentication before handling user-specific data.
- Add CSV import with validation and duplicate detection.
- Add role-based permissions and audit logging.
- Connect a Power BI report to a separately prepared sample dataset.
- Add pagination and more comprehensive tests.

## Security notes

This starter app is intended for local learning. Before deployment, set a strong `SECRET_KEY`, disable debug mode, add authentication and CSRF protection, validate uploads, configure production database credentials securely, and review privacy/security requirements. Never upload real financial or personal data to a public repository.

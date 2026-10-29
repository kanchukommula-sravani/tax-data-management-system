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

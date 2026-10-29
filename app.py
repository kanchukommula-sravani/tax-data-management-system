from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import csv
import io
import os

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tax_records.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    taxable_amount = db.Column(db.Numeric(12, 2), nullable=False)
    tax_rate = db.Column(db.Numeric(5, 2), nullable=False, default=Decimal("0.00"))
    tax_amount = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaction {self.id}: {self.description}>"


def money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))


def parse_transaction(form):
    description = form.get("description", "").strip()
    category = form.get("category", "").strip()
    date_text = form.get("transaction_date", "").strip()

    if not description or not category or not date_text:
        raise ValueError("Date, description, and category are required.")
    if len(description) > 160 or len(category) > 80:
        raise ValueError("Description or category is too long.")

    try:
        transaction_date = date.fromisoformat(date_text)
        amount = money(form.get("taxable_amount", ""))
        rate = Decimal(form.get("tax_rate", "")).quantize(Decimal("0.01"))
    except (ValueError, InvalidOperation):
        raise ValueError("Enter a valid date, taxable amount, and tax rate.")

    if amount < 0:
        raise ValueError("Taxable amount cannot be negative.")
    if rate < 0 or rate > 100:
        raise ValueError("Tax rate must be between 0 and 100.")

    tax_amount = (amount * rate / Decimal("100")).quantize(Decimal("0.01"))
    return {
        "transaction_date": transaction_date,
        "description": description,
        "category": category,
        "taxable_amount": amount,
        "tax_rate": rate,
        "tax_amount": tax_amount,
    }


@app.route("/")
def dashboard():
    transactions = Transaction.query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).limit(8).all()
    count = db.session.query(func.count(Transaction.id)).scalar() or 0
    taxable_total = db.session.query(func.coalesce(func.sum(Transaction.taxable_amount), 0)).scalar()
    tax_total = db.session.query(func.coalesce(func.sum(Transaction.tax_amount), 0)).scalar()

    month_rows = (
        db.session.query(
            func.strftime("%Y-%m", Transaction.transaction_date).label("month"),
            func.sum(Transaction.taxable_amount).label("taxable"),
            func.sum(Transaction.tax_amount).label("tax"),
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    chart_labels = [row.month for row in month_rows if row.month]
    chart_taxable = [float(row.taxable or 0) for row in month_rows if row.month]
    chart_tax = [float(row.tax or 0) for row in month_rows if row.month]

    return render_template(
        "dashboard.html",
        transactions=transactions,
        count=count,
        taxable_total=money(taxable_total),
        tax_total=money(tax_total),
        chart_labels=chart_labels,
        chart_taxable=chart_taxable,
        chart_tax=chart_tax,
    )


@app.route("/transactions")
def transactions():
    search = request.args.get("q", "").strip()
    query = Transaction.query
    if search:
        query = query.filter(
            db.or_(
                Transaction.description.ilike(f"%{search}%"),
                Transaction.category.ilike(f"%{search}%"),
            )
        )
    records = query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).all()
    return render_template("transactions.html", transactions=records, search=search)


@app.route("/transactions/new", methods=["GET", "POST"])
def new_transaction():
    if request.method == "POST":
        try:
            record = Transaction(**parse_transaction(request.form))
            db.session.add(record)
            db.session.commit()
            flash("Transaction added successfully.", "success")
            return redirect(url_for("transactions"))
        except ValueError as error:
            flash(str(error), "error")
    return render_template("transaction_form.html", transaction=None, today=date.today().isoformat())


@app.route("/transactions/<int:transaction_id>/edit", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    record = Transaction.query.get_or_404(transaction_id)
    if request.method == "POST":
        try:
            for key, value in parse_transaction(request.form).items():
                setattr(record, key, value)
            db.session.commit()
            flash("Transaction updated successfully.", "success")
            return redirect(url_for("transactions"))
        except ValueError as error:
            flash(str(error), "error")
    return render_template("transaction_form.html", transaction=record, today=date.today().isoformat())


@app.post("/transactions/<int:transaction_id>/delete")
def delete_transaction(transaction_id):
    record = Transaction.query.get_or_404(transaction_id)
    db.session.delete(record)
    db.session.commit()
    flash("Transaction deleted.", "success")
    return redirect(url_for("transactions"))


@app.route("/reports/export.csv")
def export_csv():
    records = Transaction.query.order_by(Transaction.transaction_date.asc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Date", "Description", "Category", "Taxable Amount", "Tax Rate (%)", "Calculated Tax"])
    for record in records:
        writer.writerow([
            record.id, record.transaction_date.isoformat(), record.description, record.category,
            f"{record.taxable_amount:.2f}", f"{record.tax_rate:.2f}", f"{record.tax_amount:.2f}"
        ])
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=tax_transactions.csv"
    return response


@app.route("/reports/monthly")
def monthly_report():
    rows = (
        db.session.query(
            func.strftime("%Y-%m", Transaction.transaction_date).label("month"),
            func.count(Transaction.id).label("count"),
            func.sum(Transaction.taxable_amount).label("taxable"),
            func.sum(Transaction.tax_amount).label("tax"),
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    return render_template("monthly_report.html", rows=rows)


@app.cli.command("init-db")
def init_db():
    """Create database tables."""
    with app.app_context():
        db.create_all()
    print("Database tables created.")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")

import pytest
from app import app, db, Transaction


@pytest.fixture()
def client(tmp_path):
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{tmp_path / 'test.db'}",
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Tax data at a glance" in response.data


def test_create_transaction_and_calculate_tax(client):
    response = client.post("/transactions/new", data={
        "transaction_date": "2026-01-15",
        "description": "Sample consulting",
        "category": "Consulting",
        "taxable_amount": "1000.00",
        "tax_rate": "5",
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        record = Transaction.query.filter_by(description="Sample consulting").first()
        assert record is not None
        assert float(record.tax_amount) == 50.0


def test_reject_negative_amount(client):
    response = client.post("/transactions/new", data={
        "transaction_date": "2026-01-15",
        "description": "Invalid record",
        "category": "Other",
        "taxable_amount": "-100",
        "tax_rate": "5",
    }, follow_redirects=True)
    assert b"Taxable amount cannot be negative" in response.data
    with app.app_context():
        assert Transaction.query.filter_by(description="Invalid record").first() is None


def test_csv_export(client):
    response = client.get("/reports/export.csv")
    assert response.status_code == 200
    assert b"Taxable Amount" in response.data

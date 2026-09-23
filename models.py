from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Applied")
    job_url = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
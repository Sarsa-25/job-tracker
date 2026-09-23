from flask import Flask, request, render_template
from models import db, Application
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route("/")
def home():
    return "Job Tracker is running!"

@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        company = request.form["company"]
        position = request.form["position"]
        application_date = datetime.strptime(request.form["application_date"], "%Y-%m-%d").date()
        new_app = Application(company=company, position=position, application_date=application_date)
        db.session.add(new_app)
        db.session.commit() 
        return "Application added!"
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
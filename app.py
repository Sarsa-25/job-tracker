from flask import Flask
from models import db, Application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route("/")
def home():
    return "Job Tracker is running!"

if __name__ == "__main__":
    app.run(debug=True)
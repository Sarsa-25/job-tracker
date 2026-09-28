from flask import Flask, request, render_template, redirect
from models import db, Application
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route("/")
def home():
    search_query = request.args.get("search")
    status_filter = request.args.get("status")


    applications_query = Application.query

    if search_query:
        applications_query  = applications_query.filter(Application.company.contains(search_query))

    if status_filter:
        applications_query  = applications_query.filter(Application.status == status_filter)
    
    applications = applications_query.all()
    
    total = Application.query.count()
    applied = Application.query.filter_by(status="Applied").count()
    interview = Application.query.filter_by(status="Interview").count()
    rejected = Application.query.filter_by(status="Rejected").count()
    offer = Application.query.filter_by(status="Offer").count()
    return render_template("index.html", applications=applications, total=total, applied=applied, interview=interview, rejected=rejected, offer=offer)


@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        company = request.form["company"]
        position = request.form["position"]
        application_date = datetime.strptime(request.form["application_date"], "%Y-%m-%d").date()
        status = request.form["status"]
        job_url = request.form.get("job_url") or None
        notes = request.form.get("notes") or None
        deadline_str = request.form.get("deadline")

        if deadline_str:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        else:
            deadline = None
        
        new_app = Application(company=company, position=position, application_date=application_date, status=status, job_url=job_url, notes=notes, deadline=deadline)
        db.session.add(new_app)
        db.session.commit() 
        return redirect("/")
    return render_template("add.html")


@app.route("/edit/<int:app_id>", methods=["GET", "POST"])
def edit_application(app_id):
    app_to_edit = Application.query.get_or_404(app_id)
    
    if request.method == "POST":
        app_to_edit.company = request.form["company"]
        app_to_edit.position = request.form["position"]
        app_to_edit.application_date = datetime.strptime(request.form["application_date"], "%Y-%m-%d").date()
        app_to_edit.status = request.form["status"]
        app_to_edit.job_url = request.form.get("job_url") or None
        app_to_edit.notes = request.form.get("notes") or None
        deadline_str = request.form.get("deadline")       
        if deadline_str:
            app_to_edit.deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        else:
            app_to_edit.deadline = None
        db.session.commit()
        

        return redirect("/")

    return render_template("edit.html", application=app_to_edit)


@app.route("/delete/<int:app_id>")
def delete_application(app_id):
    application = Application.query.get(app_id)
    db.session.delete(application)
    db.session.commit()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
import sys
if sys.version_info.major < 3:
    exit("use python 3")

from flask import Flask
from flask import render_template

from flask_sqlalchemy import SQLAlchemy

'''
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
'''

app = Flask(__name__)
app.secret_key = "swordfish"

app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://evensch:swordfish@localhost/evensch"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class person(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    guardian_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    contact_info = db.Column(db.String)

    events = db.relationship("person_event_role", back_populates="person")

class role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

class place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

class timeslot(db.Model):
    __tablename__ = "timeslots"

    id = db.Column(db.Integer, primary_key=True)
    starts = db.Column(db.DateTime)
    ends = db.Column(db.DateTime)

class event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    timeslot_id = db.Column(db.Integer, db.ForeignKey("timeslots.id"))

    persons = db.relationship("person_event_role", back_populates="event")

class person_event_role(db.Model):
    __tablename__ = "persons_events_roles"

    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    person = db.relationship("person", back_populates="events")
    event = db.relationship("event", back_populates="persons")

'''
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(app, name="evensch", template_mode="bootstrap3")
admin.add_view(ModelView(person, db.session))
admin.add_view(ModelView(role, db.session))
admin.add_view(ModelView(place, db.session))
admin.add_view(ModelView(timeslot, db.session))
admin.add_view(ModelView(event, db.session))
'''

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/join")
def join():
    return render_template("join.html")

@app.route("/create")
def create():
    return render_template("create.html")

if __name__ == "__main__":
    import sys
    if "--drop" in sys.argv:
        db.drop_all()
    if "--create" in sys.argv:
        db.create_all()

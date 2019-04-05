from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://evensch:swordfish@localhost/evensch"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class person(db.Model):
    __tablename__ = "persons"

    id = db.Column(db.Integer, primary_key=True)
    legal_name = db.Column(db.String)
    guardian_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    contact_info = db.Column(db.String)

class year(db.Model):
    __tablename__ = "years"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String)

class day(db.Model):
    __tablename__ = "days"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)

class validity(db.Model):
    __tablename__ = "validities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    year_id = db.Column(db.Integer, db.ForeignKey("years.id"))

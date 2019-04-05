from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import schema as db

app = Flask(__name__)
app.secret_key = "swordfish"

app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(app, name="evensch", template_mode="bootstrap3")
admin.add_view(ModelView(db.person, db.session))
admin.add_view(ModelView(db.year, db.session))
admin.add_view(ModelView(db.day, db.session))
admin.add_view(ModelView(db.validity, db.session))

app.run()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from jobs.models import User, Source
from jobs.config import DB_PATH


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH  # read local value for sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456790'


db = SQLAlchemy(app)

admin = Admin(app, name='jobs', template_mode='bootstrap3')
admin.add_view(ModelView(Source, db.session))

import jobs.views
views.startSearch

import jobs.searchbot

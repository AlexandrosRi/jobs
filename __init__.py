from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from jobs.models import User, Source


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite'  # read local value for sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456790'


db = SQLAlchemy(app)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Source, db.session))

import jobs.views
views.search

import jobs.searchbot

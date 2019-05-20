from flask import Flask, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'

db = SQLAlchemy(app)
admin = Admin(app, name='microblog', template_mode='bootstrap3')


class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    api_key = db.Column(db.String)
    network_id = db.Column(db.String)


admin.add_view(ModelView(Site, db.session))


@app.route('/')
def index():
    return render_template('index.html', sites=Site.query.all())


@app.route('/fix/<site_id>')
def fix_firewall(site_id):
    site = Site.query.get(site_id)
    resp = requests.get('https://kasownik.hackerspace.pl/api/judgement/%s.json' % (site.api_key,))

    return resp.json()['status']


@app.route('/break/<site_id>')
def break_firewall(site_id):
    return site_id

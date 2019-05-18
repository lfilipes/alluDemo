import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from . import comp_dash
from . import instant_dash
from . import table_dash
from . import pump_dash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'

instantDash = instant_dash.Add_Dash(app)
compDash = comp_dash.Add_Dash(app)
tableDash = table_dash.Add_Dash(app)
pumpDash = pump_dash.Add_Dash(app)

### for SQLite ###################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

### For PostgresSQL #############################
# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'postgres',
#     'db': 'allu_iot',
#     'host': 'localhost',
#     'port': '5432',
# }
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

###### END DATABASE SETUP ######

###### LOGIN SETUP #############
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

###### END LOGIN SETUP #########

###### BLUEPRINTs SETUP #############

from AlluIoT.core.views import core
from AlluIoT.users.views import users
from AlluIoT.error_pages.handlers import error_pages


app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)


###### END BLUEPRINTs SETUP #########



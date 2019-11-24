"""
Module for initialization different kinds of instances (flask app, database,
manager.
"""
import logging
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

APP = Flask(__name__)
API = Api(APP)

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2:' \
                                        '//postgres:admin@127.0.0.1:5432/HistoryDB'


DB = SQLAlchemy(APP)
MARSHMALLOW = Marshmallow(APP)
MIGRATE = Migrate(APP, DB)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

"""
Module for initialization different kinds of instances (flask app, database,
manager etc).
"""
import os
import logging.config
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

APP = Flask(__name__)
API = Api(APP)

POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'HistoryDB',
    'host': 'db',
    'port': '5432',
}

APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


DB = SQLAlchemy(APP)
MARSHMALLOW = Marshmallow(APP)
MIGRATE = Migrate(APP, DB)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

# CONFIG_FILE_PATH = fr"{os.getcwd()}\history_service\configs\logging.conf"
# logging.config.fileConfig(CONFIG_FILE_PATH)
LOGGER = logging.getLogger('history_service')
LOGGER.setLevel(logging.INFO)

from history_service.models.history_model import History
from history_service.models.filter_model import Filter

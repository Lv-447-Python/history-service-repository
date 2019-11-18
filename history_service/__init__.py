"""
Module for initialization different kinds of instances (flask app, database,
manager, logger.
"""
import logging
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:admin@127.0.0.1:5432/HistoryDB'


db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

logger = logging.basicConfig(level=logging.DEBUG)


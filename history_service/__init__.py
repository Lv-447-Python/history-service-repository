"""axios({
            headers: {'Content-Type': 'form-data' },
            method: 'put',
            url: 'http://0.0.0.0:80/filtering/' + props.currentFileId,
            data: filters,
        })
            .then(response => {
                let filteringResult = response.data['result'];
                console.log(filteringResult);
                props.responseResult(filteringResult)
            });
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
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

APP = Flask(__name__)
API = Api(APP)
CORS(APP, supports_credentials=True)

POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'HistoryDB',
    'host': 'db',
    'port': '5432',
}

JWT = JWTManager(APP)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2:' \
                                        '//%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = 'jwt-secret-string'
APP.config['JWT_TOKEN_LOCATION'] = ['cookies']


DB = SQLAlchemy(APP)
MARSHMALLOW = Marshmallow(APP)
MIGRATE = Migrate(APP, DB)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

from history_service.models.history_model import History
from history_service.models.filter_model import Filter

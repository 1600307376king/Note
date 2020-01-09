#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from blueprint_reg import app
from main import db
import logging


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('runserver', Server(host='0.0.0.0', port=5000))
manager.add_command('db', MigrateCommand)
@manager.option('-s', '--setting', dest='setting', default='development')
def hello(setting):
    manager.app(setting=setting)


if __name__ == '__main__':
    handler = logging.FileHandler('./logs/flask.log', encoding='UTF-8')
    handler.setFormatter(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    )
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    manager.run()
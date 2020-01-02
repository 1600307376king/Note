#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask_script import Manager, Server, Command
from main import app
import logging


manager = Manager(app)

manager.add_command('runserver', Server(host='0.0.0.0', port=5000))
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
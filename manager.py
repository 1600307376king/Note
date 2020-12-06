#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask_script import Manager, Server, Command
from flask_migrate import Migrate, MigrateCommand
from blueprint_reg import app, db
import logging


manager = Manager(app)


@manager.option('-s', '--setting', dest='setting', default='development')
def hello(setting):
    manager.app(setting=setting)


def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=3).run(tests)


migrate = Migrate(app, db)

manager.add_command('runserver', Server(host='0.0.0.0', port=5000))
manager.add_command('db', MigrateCommand)
manager.add_command('test', Command(test))


if __name__ == '__main__':
    handler = logging.FileHandler('./logs/flask.log', encoding='UTF-8')
    handler.setFormatter(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    )
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    manager.run()

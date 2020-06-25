# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, Blueprint
from tests_backend import commands
from tests_backend.extensions import db, migrate, mail
from tests_backend.api.restplus import api
from tests_backend.api.endpoints import themes_route, questions_route, admin_route, answers_route
from tests_backend.settings import ProdConfig
from flask_cors import CORS

def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(themes_route)
    api.add_namespace(questions_route)
    api.add_namespace(admin_route)
    api.add_namespace(answers_route)
    app.register_blueprint(blueprint)
    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.total_delete)
    app.cli.add_command(commands.init_data)


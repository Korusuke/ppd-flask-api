# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from ppd.files.files import files_bp
from ppd.jobs.jobs import jobs_bp
from ppd.extensions import cors


def create_app(config_object):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(files_bp, origins=origins)
    cors.init_app(jobs_bp, origins=origins)

    app.register_blueprint(files_bp, url_prefix='/files')
    app.register_blueprint(jobs_bp, url_prefix='/jobs')

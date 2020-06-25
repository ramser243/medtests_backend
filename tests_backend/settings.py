# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env
import os


class BaseConfig(object):
    env = Env()
    env.read_env()

    ENV = env.str('FLASK_ENV', default='production')
    DEBUG = ENV == 'development'
    DB_NAME = 'dev.db'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    LINKS_PATH = os.path.abspath(os.path.join(APP_DIR, "scripts", "links.txt"))
    DB_PATH = os.path.join(os.environ.get("DB_FOLDER", PROJECT_ROOT), DB_NAME)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", 'sqlite:///{0}'.format(DB_PATH))
    SECRET_KEY = env.str('SECRET_KEY')
    TESTS_LINKS_PAGE_URL = env.str('TESTS_LINKS_PAGE_URL', default=None)
    BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=13)
    DEBUG_TB_ENABLED = DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER=env.str('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT=env.str('MAIL_PORT', default=465)
    MAIL_USE_TLS=env.str('MAIL_USE_TLS', default=False)
    MAIL_USERNAME=env.str('MAIL_USERNAME', default=None)
    MAIL_PASSWORD=env.str('MAIL_PASSWORD', default=None)

    ADMIN_LOGIN=env.str('ADMIN_LOGIN', default=None)
    ADMIN_PASSWORD=env.str('ADMIN_PASSWORD', default=None)

class ProdConfig(BaseConfig):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False


class DevConfig(BaseConfig):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    UNSAFE_SUPERUSER_MODE = 1


import os
from datetime import timedelta


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    DEBUG = True


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    DEBUG = False


config_by_name = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}

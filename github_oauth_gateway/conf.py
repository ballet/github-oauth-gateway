import os


class Config:
    HOMEPAGE = 'https://github.com/HDI-Project/github-oauth-gateway'
    APP_DOMAIN = os.getenv('APP_DOMAIN', '')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')


class TestConfig:
    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'client_secret'

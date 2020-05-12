import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    ACCESS_CODE_TIMEOUT = 60
    ACCESS_CODE_POLL_INTERVAL = 5


class TestConfig:
    CLIENT_ID = 'client_id'
    CLIENT_SECRET = 'client_secret'

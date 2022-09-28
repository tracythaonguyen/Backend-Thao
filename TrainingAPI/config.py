import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    RUN_SETTING = {
        'host': os.environ.get('SERVER_HOST', 'localhost'),
        'port': int(os.environ.get('SERVER_PORT', 8080)),
        'debug': False,
        "access_log": True,
        "auto_reload": True,
        'workers': 1
    }

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
    EXPIRATION_JWT = 3600  # seconds

    REDIS = 'redis://localhost:6379/0'


class LocalDBConfig:
    pass


class RemoteDBConfig:
    pass


class MongoDBConfig:
    USERNAME = os.environ.get("MONGO_USERNAME") or "admin"
    PASSWORD = os.environ.get("MONGO_PASSWORD") or "admin123"
    HOST = os.environ.get("MONGO_HOST") or "localhost"
    PORT = os.environ.get("MONGO_PORT") or "27017"
    DATABASE = os.environ.get("MONGO_DATABASE") or "example_db"

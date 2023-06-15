"""Configuration file for the Flask app."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration."""
    SECRET_KEY=os.environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


Config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

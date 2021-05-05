class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = '$Z4v&Xv!Pt#TWFc*e$sMJTa5K9MN*WCD'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

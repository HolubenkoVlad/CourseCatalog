from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.ProductionConfig')

    with app.app_context():
        import app.catalog.routes as CatalogRoute
        app.register_blueprint(CatalogRoute.catalog)

    return app

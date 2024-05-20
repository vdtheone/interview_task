from flask import Flask
from config import Config
from src.routes.user import user_bp
from src.routes.product import product_bp
from src.database import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(product_bp, url_prefix='/product')
    return app

app = create_app()

if __name__=='__main__':
    app.run(debug=True)


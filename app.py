from flask import Flask
from models import db
from config import Config
from flask_jwt_extended import JWTManager
from controllers.usuario_controller import usuario_bp
from controllers.produto_controller import produto_bp
from controllers.cliente_controller import cliente_bp
from controllers.pedido_controller import pedido_bp
from controllers.detalhepedido_controller import detalhePedido_bp
from controllers.categoriaproduto_controllers import categoriaProduto_bp
from instance.config_jwt import jwt

def criar_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app) 

   
    app.register_blueprint(usuario_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(detalhePedido_bp)
    app.register_blueprint(categoriaProduto_bp)

   
    with app.app_context():
        db.create_all()

    return app  

if __name__ == '__main__':
    app = criar_app()
    app.run(debug=True)

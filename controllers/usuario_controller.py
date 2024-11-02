from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Usuario

usuario_bp = Blueprint('usuarios', __name__)

users = {"1": "1", "2": "2"}

@usuario_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('usuario')
    password = request.json.get('senha')
    if username not in users or users[username] != password:
        return jsonify({"msg": "Usuário ou senha incorretos"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@usuario_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(Logged_in_as=current_user), 200



@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    
    usuario = request.json
    novo_usuario = Usuario(usuario_login=usuario['usuario_login'], usuario_senha=usuario['usuario_senha'])
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({'id': novo_usuario.usuario_id, 'nome': novo_usuario.usuario_login}), 201

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()

    return jsonify([{'ID': p.usuario_id, 'Nome': p.usuario_login, 'Senha': p.usuario_senha} for p in usuarios]), 200 

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'Mensagem': 'Usuário não encontrado'}), 404

    usuario.usuario_login = dados['usuario_login']
    db.session.commit()

    return jsonify({'Usuário alterado': usuario.usuario_login})

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404 
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário excluído com sucesso'}), 200 




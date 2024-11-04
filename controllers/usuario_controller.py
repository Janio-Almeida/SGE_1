
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Usuario

usuario_bp = Blueprint('usuarios', __name__)



@usuario_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    usuario_login = dados.get('usuario_login')
    usuario_senha = dados.get('usuario_senha')

 
    if not usuario_login or not usuario_senha:
        return jsonify({'msg': 'Usuário e senha são obrigatórios'}), 400

    usuario = Usuario.query.filter_by(usuario_login=usuario_login).first()

    if not usuario or usuario.usuario_senha != usuario_senha:
        return jsonify({'msg': 'Usuário ou senha incorretos'}), 401


    access_token = create_access_token(identity=usuario_login)
    return jsonify(access_token=access_token), 200

@usuario_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(Logged_in_as=current_user), 200


@usuario_bp.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    
    dados = request.json
    usuario_login = dados.get('usuario_login')
    usuario_senha = dados.get('usuario_senha')

    if Usuario.query.filter_by(usuario_login=usuario_login).first():
        return jsonify({"msg": "Usuário já existe"}), 409

    novo_usuario = Usuario(usuario_login=usuario_login, usuario_senha=usuario_senha)
    db.session.add(novo_usuario)
    db.session.commit()

    
    return jsonify({'usuario_id': novo_usuario.usuario_id, 'usuario_login': novo_usuario.usuario_login}), 201

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()

    return jsonify([{'usuario_id': p.usuario_id, 'usuario_login': p.usuario_login, 'usuario_senha': p.usuario_senha} for p in usuarios]), 200 

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    dados = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'Mensagem': 'Usuário não encontrado'}), 404

    if 'usuario_login' in dados:
        novo_login = dados['usuario_login']
        usuario_existente = Usuario.query.filter_by(usuario_login=novo_login).first()
        
        if usuario_existente and usuario_existente.usuario_id != id:
            return jsonify({'Mensagem': 'Nome de login já em uso por outro usuário.'}), 400
        
        usuario.usuario_login = novo_login  

    if 'usuario_senha' in dados:
        usuario.usuario_senha = dados['usuario_senha'] 

    db.session.commit()

    return jsonify({'Mensagem': f'Usuário alterado para: {usuario.usuario_login}'}), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404 
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário excluído com sucesso'}), 200 

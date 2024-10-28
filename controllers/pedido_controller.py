from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Pedido


pedido_bp = Blueprint('pedidos', __name__)


@pedido_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    
    pedido = request.json

    _data_compra = datetime.strptime(pedido['data_compra'], '%Y-%m-%d').date()

    novo_pedido = Pedido(data_compra=_data_compra,
                           cliente_id=pedido['cliente_id'])
    db.session.add(novo_pedido)
    db.session.commit()
    
    return jsonify({'id': novo_pedido.pedido_id, 'data_compra': novo_pedido.data_compra}), 201

@pedido_bp.route('/pedidos', methods=['GET'])
def listar_produtos():
    pedidos = Pedido.query.all()

    return jsonify([{'ID': p.pedido_id, 'Nome': p.data_compra} for p in pedidos]), 200 

# @produto_bp.route('/produtos/<int:id>', methods=['PUT'])
# def atualizar_produto(id):
#     dados = request.json
#     produto = Produto.query.get(id)

#     if not produto:
#         return jsonify({'Mensagem': 'Produto não encontrado'}), 404

#     produto.produto_nome = dados['produto_nome']
#     db.session.commit()

#     return jsonify({'Produto alterado': produto.produto_nome})

# @produto_bp.route('/produtos/<int:id>', methods=['DELETE'])
# def excluir_produto(id):
#     #dados = request.json
#     produto = Produto.query.get(id)

#     if not produto:
#         return jsonify({'Mensagem': 'Produto não encontrado'})
    
#     db.session.delete(produto)
#     db.session.commit()

#     return jsonify({'Produto excluido'}), 200
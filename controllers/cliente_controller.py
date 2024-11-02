from flask import Blueprint, request, jsonify
from models import db, Cliente, Produto, Pedido, DetalhePedido

cliente_bp = Blueprint('clientes', __name__)

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    cliente = request.json
    novo_cliente = Cliente(cliente_nome=cliente['cliente_nome'],
                           cliente_email=cliente['cliente_email'])
    db.session.add(novo_cliente)
    db.session.commit()
    
    return jsonify({
        'id': novo_cliente.cliente_id,
        'nome': novo_cliente.cliente_nome,
        'email': novo_cliente.cliente_email
    }), 201

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    
    return jsonify([{'ID': c.cliente_id, 'Nome': c.cliente_nome} for c in clientes]), 200

@cliente_bp.route('/clienteproduto', methods=['GET'])
def relatorio():
   
    relatorio = db.session.query(
        Cliente.clientenome.label('cliente_nome'),
        Produto.produto_nome.label('produto_nome')
    ).join(Pedido, Pedido.cliente_id == Cliente.cliente_id) \
     .join(DetalhePedido, DetalhePedido.dp_pedido_id == Pedido.pedido_id) \
     .join(Produto, Produto.produto_id == DetalhePedido.dp_produto_id) \
     .all()

 
    pedido_lista = [{'produto_nome': c.produto_nome, 'cliente_nome': c.cliente_nome} for c in relatorio]

    return jsonify(pedido_lista), 200

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)  

    if not cliente:
        return jsonify({'mensagem': 'Cliente não encontrado'}), 404 

    db.session.delete(cliente) 
    db.session.commit()  

    return jsonify({'mensagem': 'Cliente excluído com sucesso'}), 200 

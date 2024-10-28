from models import db


class CategoriaProduto(db.Model):
    __tablename__ = 'categoria_produto'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    nome_categoria = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<CategoriaProduto {self.nome_categoria}>'
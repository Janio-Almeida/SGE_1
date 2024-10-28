import unittest
from app import create_app  # Altere para o nome do seu aplicativo
from models import db, Usuario  # Altere para o caminho correto da sua classe

class TestUsuarioModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')  
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all() 

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()  
        cls.app_context.pop()

    def test_criar_usuario(self):
        usuario = Usuario(usuario_login='teste', usuario_senha='senha123')
        db.session.add(usuario)
        db.session.commit()

        
        self.assertEqual(usuario.usuario_login, 'teste')
        self.assertEqual(usuario.usuario_senha, 'senha123')

        usuario_db = Usuario.query.filter_by(usuario_login='teste').first()
        self.assertIsNotNone(usuario_db)
        self.assertEqual(usuario_db.usuario_id, usuario.usuario_id)

if __name__ == "__main__":
    unittest.main()
import unittest
from models import Cliente 

class TestCliente(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(1, "João", "joao@example.com")

    def test_cliente_id(self):
        self.assertEqual(self.cliente.id, 1)

    def test_cliente_nome(self):
        self.assertEqual(self.cliente.nome, "João")

    def test_cliente_email(self):
        self.assertEqual(self.cliente.email, "joao@example.com")

    def test_str(self):
        self.assertEqual(str(self.cliente), "Cliente(1, João, joao@example.com)")

if __name__ == "__main__":
    unittest.main()
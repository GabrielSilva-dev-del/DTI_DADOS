import unittest
from Py import main

class TestPy(unittest.TestCase):
    def test_main(self):
        # Teste básico para verificar se o script principal executa sem erros
        try:
            main()
        except Exception as e:
            self.fail(f"main() falhou com a exceção: {e}")

if __name__ == "__main__":
    unittest.main()
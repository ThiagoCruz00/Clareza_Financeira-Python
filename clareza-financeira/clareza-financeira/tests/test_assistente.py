import unittest

from src.assistente import AssistenteFinanceiro


class TestAssistenteFinanceiro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assistente = AssistenteFinanceiro()

    def test_responde_sobre_orcamento(self):
        resposta = self.assistente.responder("Como posso organizar meu dinheiro?")
        self.assertIn("orçamento", resposta.lower())
        self.assertIn("Próximo passo", resposta)

    def test_bloqueia_dados_sensiveis(self):
        resposta = self.assistente.responder("Posso informar minha senha para você?")
        self.assertIn("não compartilhe", resposta.lower())

    def test_informa_quando_nao_sabe(self):
        resposta = self.assistente.responder("Qual será a cotação do dólar amanhã?")
        self.assertIn("não encontrei informação suficiente", resposta.lower())

    def test_trata_pergunta_vazia(self):
        resposta = self.assistente.responder("   ")
        self.assertIn("Escreva uma dúvida", resposta)


if __name__ == "__main__":
    unittest.main()

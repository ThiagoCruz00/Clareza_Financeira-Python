from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any


class AssistenteFinanceiro:
    """Assistente educativo baseado em uma base de conhecimento local.

    O assistente não inventa respostas: ele só responde quando encontra
    evidência suficiente na base e orienta a pessoa a buscar ajuda oficial
    quando a pergunta exige uma ação que ele não pode executar.
    """

    PALAVRAS_SENSIVEIS = {
        "senha", "password", "token", "codigo", "código", "cvv",
        "cartao", "cartão", "cpf", "login", "autenticacao", "autenticação"
    }

    def __init__(self, caminho_base: str | Path | None = None) -> None:
        caminho = Path(caminho_base or Path(__file__).parents[1] / "data" / "base_conhecimento.json")
        with caminho.open(encoding="utf-8") as arquivo:
            self.base: dict[str, Any] = json.load(arquivo)
        self.artigos = self.base["artigos"]

    @staticmethod
    def normalizar(texto: str) -> str:
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(letra for letra in texto if not unicodedata.combining(letra))
        return re.sub(r"[^a-z0-9 ]", " ", texto.lower())

    def _pontuar(self, pergunta: str, artigo: dict[str, Any]) -> int:
        texto = self.normalizar(pergunta)
        tokens = set(texto.split())
        melhor = 0
        for consulta in artigo["perguntas"]:
            termos = set(self.normalizar(consulta).split())
            melhor = max(melhor, len(tokens & termos))
        if self.normalizar(artigo["titulo"]) in texto:
            melhor += 2
        return melhor

    def buscar(self, pergunta: str) -> tuple[dict[str, Any] | None, int]:
        resultados = [(self._pontuar(pergunta, artigo), artigo) for artigo in self.artigos]
        pontuacao, artigo = max(resultados, key=lambda item: item[0])
        return (artigo, pontuacao) if pontuacao >= 1 else (None, 0)

    def responder(self, pergunta: str) -> str:
        pergunta = pergunta.strip()
        if not pergunta:
            return "Escreva uma dúvida, por exemplo: 'como começar um orçamento?'"

        texto_normalizado = self.normalizar(pergunta)
        if any(self.normalizar(palavra) in texto_normalizado for palavra in self.PALAVRAS_SENSIVEIS):
            return ("Por segurança, não compartilhe senhas, códigos, CVV, CPF completo ou dados de cartão. "
                    "Posso explicar boas práticas de segurança financeira sem receber seus dados pessoais.")

        artigo, pontuacao = self.buscar(pergunta)
        if artigo is None:
            return ("Ainda não encontrei informação suficiente na minha base para responder com segurança. "
                    "Tente perguntar sobre orçamento, reserva de emergência, dívidas, compras ou golpes. "
                    "Para decisões específicas, procure uma instituição ou profissional habilitado.")

        aviso = self.base["avisos"][0]
        return (f"**{artigo['titulo']}**\n\n{artigo['resposta']}\n\n"
                f"**Próximo passo:** {artigo['proximo_passo']}\n\n"
                f"_Nota: {aviso}_")


def executar_terminal() -> None:
    assistente = AssistenteFinanceiro()
    print("Clareza Financeira — Assistente educativo")
    print("Digite 'sair' para encerrar. Não informe dados pessoais.\n")
    while True:
        pergunta = input("Você: ").strip()
        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Clareza: Até a próxima. Cuide dos seus dados e do seu orçamento!")
            break
        print(f"Clareza: {assistente.responder(pergunta)}\n")


if __name__ == "__main__":
    executar_terminal()

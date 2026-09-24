# Clareza Financeira

> Assistente virtual educativo para transformar dúvidas financeiras em próximos passos simples e seguros.

## 1. Apresentação

O **Clareza Financeira** é um protótipo de assistente virtual com inteligência artificial para pessoas que querem começar a organizar a vida financeira. Ele responde dúvidas sobre orçamento, reserva de emergência, dívidas, compras e segurança contra golpes.

Este README reúne **todo o projeto em um único arquivo**. Não é necessário manter arquivos separados para entender ou apresentar a solução. O código, a base de conhecimento, o prompt, os testes e a documentação estão organizados abaixo.

## 2. Problema

Muitas pessoas sabem que precisam organizar o dinheiro, mas não sabem qual é a primeira ação. Respostas genéricas podem confundir, enquanto recomendações sem contexto podem ser arriscadas.

O projeto resolve esse problema com uma experiência simples: a pessoa escreve uma dúvida, o assistente identifica o tema correspondente, responde em linguagem acessível e indica um próximo passo. Quando não encontra informação suficiente, ele assume a limitação em vez de inventar uma resposta.

> Este projeto é educativo. Não oferece aconselhamento financeiro personalizado, não prevê o mercado e não executa ações em contas bancárias.

## 3. Objetivos

O assistente deve:

- Entender dúvidas sobre organização financeira básica.

- Usar uma base de conhecimento controlada.

- Responder de forma clara e prática.

- Indicar um próximo passo para a pessoa usuária.

- Evitar respostas inventadas.

- Informar quando não tiver conhecimento suficiente.

- Proteger dados sensíveis.

- Orientar o contato com canais oficiais em casos de golpes.

## 4. Solução

A solução utiliza uma base de conhecimento local. Cada artigo contém um título, perguntas relacionadas, uma resposta e uma recomendação de próximo passo.

O motor do assistente normaliza acentos e caracteres, compara os termos da pergunta com os artigos e responde apenas quando encontra correspondência suficiente.

A aplicação também possui regras de segurança. Perguntas que contenham termos como senha, código, CVV, CPF, cartão ou autenticação recebem uma orientação para não compartilhar informações sensíveis.

## 5. Como executar

A solução não precisa de chave de API ou serviço externo.

Salve este README como `README.md` dentro de uma pasta ou repositório e copie o código da seção **Código completo** para um arquivo chamado `app.py`.

Depois, execute:

```bash
python app.py
```

Exemplo de perguntas:

```
Como posso organizar meu dinheiro?
Como criar uma reserva de emergência?
Estou com dívidas, o que faço?
Posso informar minha senha?
Caí em um golpe, o que devo fazer?
```

Para encerrar, digite:

```
sair
```

## 6. Código completo

Crie um arquivo chamado `app.py` e cole o código abaixo:

```python
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any


BASE_CONHECIMENTO = {
    "avisos": [
        "Este conteúdo é educativo e não substitui orientação profissional personalizada.",
        "Nunca compartilhe senhas, códigos de autenticação ou dados completos de cartão."
    ],
    "artigos": [
        {
            "id": "orcamento",
            "titulo": "Como começar um orçamento",
            "perguntas": [
                "como fazer orçamento", "organizar meu dinheiro",
                "controlar gastos", "planejar gastos"
            ],
            "resposta": (
                "Comece anotando sua renda líquida e todos os gastos por 30 dias. "
                "Separe despesas essenciais, variáveis e dívidas. Depois, defina "
                "um limite para cada categoria e revise o plano semanalmente."
            ),
            "proximo_passo": (
                "Registre hoje os últimos sete dias de gastos e classifique cada lançamento."
            )
        },
        {
            "id": "reserva",
            "titulo": "Reserva de emergência",
            "perguntas": [
                "o que é reserva de emergência", "quanto guardar",
                "reserva financeira", "dinheiro para emergência"
            ],
            "resposta": (
                "A reserva de emergência é um valor separado para imprevistos, "
                "como perda de renda ou despesas médicas. Um objetivo inicial é "
                "acumular um mês de despesas essenciais e evoluir gradualmente "
                "conforme sua estabilidade e realidade."
            ),
            "proximo_passo": (
                "Calcule suas despesas essenciais mensais e escolha um valor automático, "
                "mesmo que pequeno, para começar."
            )
        },
        {
            "id": "dividas",
            "titulo": "Organização de dívidas",
            "perguntas": [
                "como sair das dívidas", "tenho dívidas", "juros altos",
                "negociar dívida", "cartão atrasado"
            ],
            "resposta": (
                "Liste cada dívida, saldo, juros, parcela e vencimento. Priorize as "
                "que têm juros mais altos e evite assumir novas parcelas enquanto "
                "organiza o orçamento. Antes de aceitar um acordo, compare o custo "
                "total e confirme se a parcela cabe no orçamento."
            ),
            "proximo_passo": (
                "Monte uma tabela com todas as dívidas e destaque a que possui o maior custo efetivo."
            )
        },
        {
            "id": "golpes",
            "titulo": "Segurança contra golpes",
            "perguntas": [
                "caí em um golpe", "golpe", "pix suspeito", "link falso",
                "segurança financeira", "fraude"
            ],
            "resposta": (
                "Não envie senhas ou códigos e não clique em links suspeitos. Se houve "
                "uma transação não reconhecida, contate imediatamente o banco pelos "
                "canais oficiais, registre a ocorrência e guarde comprovantes. O "
                "assistente não consegue bloquear uma conta ou recuperar valores."
            ),
            "proximo_passo": (
                "Entre em contato com seu banco usando o aplicativo ou o telefone "
                "que aparece no cartão oficial, nunca o número recebido por mensagem."
            )
        },
        {
            "id": "compras",
            "titulo": "Decisão antes de comprar",
            "perguntas": [
                "posso comprar", "compra parcelada", "preciso comprar",
                "como decidir uma compra"
            ],
            "resposta": (
                "Antes de comprar, verifique se a despesa é necessária, se existe "
                "dinheiro reservado e qual será o impacto no orçamento dos próximos "
                "meses. Compare o preço à vista com o custo total parcelado e evite "
                "decidir sob pressão."
            ),
            "proximo_passo": (
                "Espere 24 horas antes de uma compra não essencial e escreva o "
                "impacto da parcela no orçamento mensal."
            )
        }
    ]
}


class AssistenteFinanceiro:
    """Assistente educativo com base de conhecimento local."""

    PALAVRAS_SENSIVEIS = {
        "senha", "password", "token", "codigo", "código", "cvv",
        "cartao", "cartão", "cpf", "login", "autenticacao", "autenticação"
    }

    def __init__(self, base: dict[str, Any] | None = None) -> None:
        self.base = base or BASE_CONHECIMENTO
        self.artigos = self.base["artigos"]

    @staticmethod
    def normalizar(texto: str) -> str:
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(letra for letra in texto if not unicodedata.combining(letra))
        return re.sub(r"[^a-z0-9 ]", " ", texto.lower())

    def pontuar(self, pergunta: str, artigo: dict[str, Any]) -> int:
        texto = self.normalizar(pergunta)
        tokens = set(texto.split())
        melhor_pontuacao = 0

        for consulta in artigo["perguntas"]:
            termos = set(self.normalizar(consulta).split())
            melhor_pontuacao = max(melhor_pontuacao, len(tokens & termos))

        if self.normalizar(artigo["titulo"]) in texto:
            melhor_pontuacao += 2

        return melhor_pontuacao

    def buscar(self, pergunta: str) -> tuple[dict[str, Any] | None, int]:
        resultados = [
            (self.pontuar(pergunta, artigo), artigo)
            for artigo in self.artigos
        ]
        pontuacao, artigo = max(resultados, key=lambda item: item[0])
        return (artigo, pontuacao) if pontuacao >= 1 else (None, 0)

    def responder(self, pergunta: str) -> str:
        pergunta = pergunta.strip()

        if not pergunta:
            return "Escreva uma dúvida, por exemplo: 'como começar um orçamento?'"

        texto_normalizado = self.normalizar(pergunta)
        palavras_proibidas = [self.normalizar(palavra) for palavra in self.PALAVRAS_SENSIVEIS]

        if any(palavra in texto_normalizado for palavra in palavras_proibidas):
            return (
                "Por segurança, não compartilhe senhas, códigos, CVV, CPF completo "
                "ou dados de cartão. Posso explicar boas práticas de segurança "
                "financeira sem receber seus dados pessoais."
            )

        artigo, _ = self.buscar(pergunta)

        if artigo is None:
            return (
                "Ainda não encontrei informação suficiente na minha base para "
                "responder com segurança. Tente perguntar sobre orçamento, "
                "reserva de emergência, dívidas, compras ou golpes. Para decisões "
                "específicas, procure uma instituição ou profissional habilitado."
            )

        aviso = self.base["avisos"][0]
        return (
            f"**{artigo['titulo']}**\n\n"
            f"{artigo['resposta']}\n\n"
            f"**Próximo passo:** {artigo['proximo_passo']}\n\n"
            f"_Nota: {aviso}_"
        )


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
```

## 7. Prompt do agente

Caso o projeto seja futuramente conectado a um modelo de linguagem, use estas instruções como prompt de sistema:

```
Você é o Clareza Financeira, um assistente educativo.
Use apenas o conteúdo recuperado da base de conhecimento.
Responda em português, com linguagem simples e sem julgamento.
Inclua uma orientação prática de próximo passo.
Se a base não trouxer evidência suficiente, diga que não sabe e não invente.
Nunca peça senhas, códigos, CVV, CPF completo ou dados de cartão.
Não prometa recuperar dinheiro, bloquear contas ou prestar aconselhamento profissional.
Em casos de golpe, oriente o contato com o banco pelos canais oficiais.
```

## 8. Base de conhecimento

A base usada pelo código contém cinco temas:

| Tema | Objetivo |
| --- | --- |
| Orçamento | Ajudar a pessoa a registrar renda e despesas |
| Reserva de emergência | Explicar como começar uma reserva |
| Dívidas | Organizar dívidas e priorizar juros altos |
| Golpes | Orientar ações seguras em caso de fraude |
| Compras | Apoiar decisões antes de uma compra |

Para adicionar um novo tema, acrescente um novo dicionário ao campo `artigos` dentro da variável `BASE_CONHECIMENTO`.

## 9. Avaliação

### Casos de teste

| Caso | Entrada | Resultado esperado |
| --- | --- | --- |
| Conhecimento | Como organizar meu dinheiro? | Resposta relacionada a orçamento |
| Segurança | Posso informar minha senha? | Bloqueio de dados sensíveis |
| Limitação | Qual será a cotação do dólar amanhã? | Fallback sem inventar informação |
| Entrada vazia | Texto em branco | Pedido para escrever uma dúvida |

### Métricas

**Cobertura de intenção:** proporção de perguntas conhecidas respondidas com o tema correto.

**Taxa de recusa segura:** proporção de perguntas sobre credenciais que são bloqueadas corretamente.

**Taxa de alucinação observada:** proporção de perguntas fora da base respondidas com informação inventada. O objetivo é manter essa taxa em zero nos testes controlados.

**Satisfação da pessoa usuária:** avaliação dada após a conversa, em uma escala de 1 a 5.

## 10. Testes automatizados

Crie um arquivo `test_app.py` com o conteúdo abaixo:

```python
import unittest
from app import AssistenteFinanceiro


class TestAssistenteFinanceiro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assistente = AssistenteFinanceiro()

    def test_responde_sobre_orcamento(self):
        resposta = self.assistente.responder("Como posso organizar meu dinheiro?")
        self.assertIn("orçamento", resposta.lower())
        self.assertIn("Próximo passo", resposta)

    def test_bloqueia_dados_sensiveis(self):
        resposta = self.assistente.responder("Posso informar minha senha?")
        self.assertIn("não compartilhe", resposta.lower())

    def test_informa_quando_nao_sabe(self):
        resposta = self.assistente.responder("Qual será a cotação do dólar amanhã?")
        self.assertIn("não encontrei informação suficiente", resposta.lower())

    def test_trata_pergunta_vazia(self):
        resposta = self.assistente.responder("   ")
        self.assertIn("Escreva uma dúvida", resposta)


if __name__ == "__main__":
    unittest.main()
```

Execute os testes com:

```bash
python -m unittest test_app.py -v
```

## 11. Pitch final

O Clareza Financeira transforma dúvidas financeiras comuns em próximos passos práticos. Seu diferencial é combinar simplicidade, base de conhecimento controlada e segurança. O assistente não tenta responder tudo: quando não possui informação suficiente, ele admite a limitação. Isso torna o protótipo mais confiável e cria uma base adequada para futuras evoluções com busca semântica, interface web e modelos de linguagem.

## 12. Limitações e próximos passos

A busca atual é lexical e pode não compreender todos os sinônimos. O projeto ainda não possui interface gráfica, histórico de conversa, personalização por perfil ou integração com instituições financeiras.

As próximas evoluções recomendadas são:

1. Ampliar a base com perguntas reais anonimizadas.

1. Adicionar revisão humana do conteúdo.

1. Criar uma interface web ou aplicativo.

1. Comparar busca lexical com busca semântica.

1. Acompanhar cobertura, segurança e satisfação.

1. Adicionar uma camada de modelo de linguagem apenas com regras de segurança bem definidas.

## 13. Privacidade

Não informe dados pessoais durante os testes. O projeto não precisa de credenciais e não armazena informações financeiras. Em caso de transação não reconhecida, procure imediatamente o banco pelos canais oficiais.

## 14. Licença

Projeto educacional para portfólio. Inclua a licença de sua preferência antes de publicar o repositório.

# Clareza Financeira

> Assistente virtual educativo para transformar dúvidas financeiras em próximos passos simples e seguros.

## Visão geral

O **Clareza Financeira** é um protótipo de assistente virtual com inteligência artificial para pessoas que querem começar a organizar a vida financeira. Nesta primeira versão, o assistente responde sobre orçamento, reserva de emergência, dívidas, compras e segurança contra golpes.

A solução foi construída para demonstrar os seis passos do desafio: documentação do agente, base de conhecimento, prompts, aplicação funcional, avaliação e pitch.

## Problema

Muitas pessoas sabem que precisam organizar o dinheiro, mas não sabem qual é a primeira ação. Respostas genéricas podem confundir, enquanto recomendações sem contexto podem ser arriscadas.

O projeto resolve esse problema com uma experiência simples: a pessoa escreve uma dúvida, o assistente localiza o tema correspondente na base de conhecimento, responde em linguagem acessível e indica um próximo passo. Quando não encontra informação suficiente, ele assume a limitação em vez de inventar uma resposta.

## Solução

O sistema utiliza uma base de conhecimento local em JSON. Cada artigo possui título, perguntas relacionadas, resposta e próximo passo. O motor normaliza a linguagem, compara termos da pergunta com os artigos e só responde quando atinge uma evidência mínima.

A aplicação também possui uma camada de segurança. Ela bloqueia perguntas que tentam compartilhar senhas, códigos, CVV, CPF ou dados de cartão. Em situações de golpe, orienta a pessoa a utilizar os canais oficiais da instituição financeira.

> Este projeto é educativo. Ele não oferece aconselhamento financeiro personalizado, não prevê mercado e não executa ações em contas bancárias.

## Demonstração

Execute:

```bash
python app.py
```

Exemplo de conversa:

```text
Você: Como posso organizar meu dinheiro?
Clareza: **Como começar um orçamento**

Comece anotando sua renda líquida e todos os gastos por 30 dias...

Próximo passo: Registre hoje os últimos sete dias de gastos...
```

Para sair, digite `sair`.

## Como executar

O projeto não exige chave de API nem serviço externo. Isso torna a demonstração reproduzível e evita o envio de dados pessoais para terceiros.

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd clareza-financeira
python app.py
```

Para executar os testes:

```bash
python -m unittest discover -s tests -v
```

## Estrutura do projeto

```text
clareza-financeira/
├── README.md
├── app.py
├── data/
│   └── base_conhecimento.json
├── docs/
│   ├── avaliacao.md
│   └── guia_do_agente.md
├── src/
│   └── assistente.py
└── tests/
    └── test_assistente.py
```

## Os seis passos do desafio

### 1. Documentação

O objetivo, o público e as regras de comportamento estão registrados em [`docs/guia_do_agente.md`](docs/guia_do_agente.md).

### 2. Base de conhecimento

A base inicial está em [`data/base_conhecimento.json`](data/base_conhecimento.json). Ela pode ser expandida com novos artigos sem alterar o motor principal.

### 3. Prompts

O prompt conceitual, as regras de segurança e o fallback estão documentados no guia do agente. A implementação atual é determinística e local; em uma versão com um modelo de linguagem, essas mesmas regras devem ser usadas como instruções de sistema.

### 4. Aplicação funcional

[`app.py`](app.py) inicia uma conversa no terminal. A lógica está separada em [`src/assistente.py`](src/assistente.py), o que facilita a evolução para uma interface web ou integração com uma API.

### 5. Avaliação e métricas

Os casos de teste e as métricas propostas estão em [`docs/avaliacao.md`](docs/avaliacao.md). A suíte automatizada verifica resposta de conhecimento, proteção contra dados sensíveis, fallback para perguntas desconhecidas e tratamento de entrada vazia.

### 6. Pitch

O Clareza Financeira reduz a distância entre uma dúvida financeira e uma ação prática. Ele é pequeno o suficiente para ser compreendido, seguro o suficiente para não solicitar credenciais e extensível o suficiente para receber novos conteúdos.

## Limitações e próximos passos

A busca atual é lexical e não compreende todos os sinônimos ou contextos. Ela não substitui uma busca semântica com embeddings nem um modelo de linguagem. Também não há persistência de conversa, autenticação, interface gráfica ou personalização por perfil.

As próximas evoluções recomendadas são adicionar perguntas reais anonimizadas, ampliar a base com revisão humana, criar uma interface web, comparar busca lexical com busca semântica e acompanhar cobertura de intenção, recusas seguras e satisfação das pessoas usuárias.

## Privacidade e segurança

Não informe dados pessoais durante os testes. O projeto não precisa de credenciais e não foi desenhado para armazenar informações financeiras. Em caso de transação não reconhecida, a pessoa deve procurar imediatamente o banco pelos canais oficiais.

## Licença

Projeto educacional para portfólio. Adapte o conteúdo e inclua a licença que preferir antes da publicação pública.

# Khanto Reservations

## O que é? 🤔

Este projeto consiste na criação de uma aplicação REST com 3 recursos principais: Propriedades, Anúncios e Reservas. Ele foi desenvolvido como parte do teste prático para vaga de desenvolvedor na Seazone.

## Ferramentas 🛠️

O projeto foi desenvolvido utilizando os frameworks Django e DRF para criação da aplicação, além de algumas de suas ferramentas internas para criação de funcionalidades como testes unitários e carregamento de fixtures. Já para o gerenciamento de pacotes e dependências foi utilizado o Poetry, ao invés de Pipenv ou similares, tendo em vista os últimos resultados de performance obtidos quando comparados.

## Como rodar? 🚀

### Pré-requisitos 📋

- Python 3.10
- Poetry
- Banco de Dados PostgreSQL

### Instalação 🔧

Após a instalação dos pré-requisitos, clone o repositório e instale as dependências com o Poetry:

```bash

$ poetry install
# Ative o virtual env (opcional)
$ poetry shell
# Se ativar, não é necessário o 'poetry run' nos próximos comandos

```

### Configuração 🔧

Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

```bash

SECRET_KEY= # Chave secreta do Django
DATABASE_URL = # URL de conexão com o banco de dados (ex: postgres://user:password@host:port/database)

```

### Migrações e fixtures 🗃️

Para criar as tabelas no banco de dados e carregar os dados iniciais, basta rodar os comandos abaixo:

```bash

$ poetry run python manage.py migrate

$ poetry run python manage.py loaddata khanto/apps/properties/fixtures/fixture_properties_announcements.json

$ poetry run python manage.py loaddata khanto/apps/reservations/fixtures/fixture_reservations.json
```

### Rodando os testes 🧪

Para rodar os testes, basta rodar os comandos abaixo:

```bash

$ poetry run python manage.py test properties
$ poetry run python manage.py test reservations

```

### Execução 🚀

Para executar o projeto, basta rodar o comando abaixo:

```bash

$ poetry run python manage.py runserver

```

## Documentação 📃

A documentação dos endpoints foi feita com Swagger e está disponível na rota `/swagger`.

## Próximos passos 📌

- Finalizar o Frontend iniciado com Vue e Buefy
- Deploy na instância pessoal da AWS do Lightsail
- Dockerizar a aplicação

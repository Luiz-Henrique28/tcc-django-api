# TCC API - Django 6.0

Esta é a API RESTful desenvolvida em Django 6.0 para fins de comparação acadêmica de desempenho (TCC).

## Tecnologias
- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL 14
- Nginx 1.25
- Docker & Docker Compose
- PgBouncer (Connection Pooling)

## Como rodar com Docker

1. Clone o repositório.
2. Copie o arquivo de ambiente padrão:
   ```bash
   cp .env.example .env
   ```
3. Suba os contêineres em segundo plano:
   ```bash
   docker compose up -d
   ```
4. Rode as migrações e o seed de dados:
   ```bash
   docker compose exec app python manage.py migrate
   docker compose exec app python manage.py seed
   ```

A API estará disponível em `http://127.0.0.1:8002`.
Para acessar via Postman, importe a coleção `postman_collection.json` inclusa na raiz.

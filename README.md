<h1 align="center">TCC — API de Catálogo de Produtos (Django 6.0)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 6.0">
  <img src="https://img.shields.io/badge/DRF-Django_REST_Framework-A30000?style=for-the-badge" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-14-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL 14">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Nginx-1.25-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx 1.25">
  <img src="https://img.shields.io/badge/PgBouncer-Connection_Pool-336791?style=for-the-badge" alt="PgBouncer">
</p>

---

## Contexto

Este repositório contém a implementação em **Django 6.0** de uma API RESTful de Catálogo de Produtos desenvolvida como parte de um Trabalho de Conclusão de Curso (TCC).

O objetivo do TCC é realizar uma **análise comparativa de desempenho** entre os frameworks **Django** e **Laravel** sob diferentes cenários de carga, com e sem o uso de *Connection Pooling* (PgBouncer). Ambas as APIs foram desenvolvidas de forma rigorosamente equivalente — com os mesmos endpoints, modelagem de dados, estrutura de resposta JSON e volume de dados — para garantir uma comparação justa e metodologicamente válida.

As métricas avaliadas nos testes são: **Latência**, **Requisições por Segundo (RPS)**, **Consumo de CPU**, **Consumo de Memória** e **Taxa de Erros**.

---

## Pré-requisitos

- Docker Desktop com backend WSL2 habilitado
- Git
- Ubuntu via WSL2 (para execução dos testes de carga)

> ⚠️ **Usuários Windows:** todos os comandos abaixo devem ser executados dentro do terminal do **Ubuntu (WSL2)**, e não pelo PowerShell ou CMD.

---

## Como Rodar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/tcc-django-api.git
cd tcc-django-api
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

### 3. Suba os contêineres
```bash
docker compose up -d
```

### 4. Rode as migrações e popule o banco de dados
```bash
docker compose exec app python manage.py migrate
docker compose exec app python manage.py seed
```

A API estará disponível em `http://127.0.0.1:8002`.

> 💡 **Seed:** O comando de seed popula o banco com **20 categorias** e **1.000 produtos** gerados com semente de aleatoriedade fixa (`random.seed(42)`), garantindo dados estatisticamente idênticos aos do repositório Laravel para fins de comparação.

---

## Testando a API

### 1. Coleção do Postman

Para testar os endpoints manualmente, importe a coleção inclusa na raiz do projeto:

1. Abra o **Postman**.
2. Clique em **Import** e selecione o arquivo `postman_collection.json`.
3. Altere a variável `{{base_url}}` para `http://127.0.0.1:8002`.
4. A variável `{{token}}` deve ser preenchida com o token obtido no *Register* ou *Login*.

> 💡 **Fluxo recomendado:** Execute primeiro o *Register* ou o *Login* para obter o token de acesso. Copie o token retornado e cole na variável `{{token}}` da coleção. As rotas de escrita estarão liberadas.

### 2. Teste rápido via cURL

```bash
# Listar produtos (rota pública)
curl -s http://127.0.0.1:8002/api/products | python3 -m json.tool

# Registrar um usuário
curl -s -X POST http://127.0.0.1:8002/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Henrique","email":"teste@tcc.com","password":"senha123"}' \
  | python3 -m json.tool
```

---

## Endpoints

### Autenticação

| Método | Rota | Auth? | Descrição |
|--------|------|-------|-----------|
| `POST` | `/api/auth/register` | ❌ | Registrar novo usuário e obter token |
| `POST` | `/api/auth/login` | ❌ | Autenticar e obter token |
| `POST` | `/api/auth/logout` | ✅ Bearer | Invalidar o token atual |

### Categorias

| Método | Rota | Auth? | Descrição |
|--------|------|-------|-----------|
| `GET` | `/api/categories` | ❌ | Listar todas as categorias |
| `GET` | `/api/categories/{id}` | ❌ | Exibir uma categoria |
| `POST` | `/api/categories` | ✅ Bearer | Criar nova categoria |
| `PUT` | `/api/categories/{id}` | ✅ Bearer | Atualizar uma categoria |
| `DELETE` | `/api/categories/{id}` | ✅ Bearer | Remover uma categoria |

### Produtos

| Método | Rota | Auth? | Descrição |
|--------|------|-------|-----------|
| `GET` | `/api/products` | ❌ | Listar produtos (paginado, 20/pág, ordenado por ID desc) |
| `GET` | `/api/products?category={id}` | ❌ | Filtrar produtos por categoria |
| `GET` | `/api/products/{id}` | ❌ | Exibir um produto |
| `POST` | `/api/products` | ✅ Bearer | Criar novo produto |
| `PUT` | `/api/products/{id}` | ✅ Bearer | Atualizar um produto |
| `DELETE` | `/api/products/{id}` | ✅ Bearer | Remover um produto |

### Formato de Resposta (JSON Padronizado)

**Listagem de produtos:**
```json
{
  "data": [ { "id": 1000, "nome": "...", "preco": "...", "estoque": 0, "categoria": { "id": 1, "nome": "..." }, "criado_em": "...", "atualizado_em": "..." } ],
  "links": { "first": "...", "last": "...", "prev": null, "next": "..." },
  "meta": { "current_page": 1, "last_page": 50, "per_page": 20, "total": 1000 }
}
```

---

## Modelagem de Dados

A API expõe dois recursos principais ligados por chave estrangeira:

**`catalog_category`**

| Campo | Tipo | Detalhe |
|-------|------|---------|
| `id` | `BIGINT PK` | Auto-incremento |
| `nome` | `VARCHAR(255)` | — |
| `descricao` | `TEXT` | Nullable |

**`catalog_product`**

| Campo | Tipo | Detalhe |
|-------|------|---------|
| `id` | `BIGINT PK` | Auto-incremento |
| `nome` | `VARCHAR(255)` | — |
| `descricao` | `TEXT` | Nullable |
| `preco` | `DECIMAL(10,2)` | — |
| `estoque` | `INTEGER` | Default 0 |
| `categoria_id` | `BIGINT FK` | → `catalog_category.id` |
| `criado_em` | `TIMESTAMP` | Gerenciado pelo Django ORM |
| `atualizado_em` | `TIMESTAMP` | Gerenciado pelo Django ORM |

---

## Decisões de Implementação

Estas decisões foram tomadas para garantir paridade com a implementação Laravel e validade metodológica do TCC:

- **`BearerTokenAuthentication` customizado:** O DRF utiliza por padrão o prefixo `Token` no cabeçalho de autorização. Para manter paridade total com o Laravel Sanctum, foi criada a classe `BearerTokenAuthentication` (em `catalog/authentication.py`) que faz o Django aceitar o prefixo `Bearer`, tornando o protocolo de autenticação idêntico entre os dois frameworks.

- **`LaravelStylePagination` customizado:** A paginação padrão do DRF retorna `count`, `next` e `previous`. Foi criada a classe `LaravelStylePagination` (em `catalog/pagination.py`) que replica exatamente a estrutura `data`, `links` e `meta` do Laravel, eliminando diferenças de formato JSON que comprometeriam a comparação.

- **`APPEND_SLASH = False`:** O Django redireciona URLs sem barra final para a versão com barra (`302 Redirect`) por padrão. Essa configuração foi desabilitada para que a API responda diretamente em `/api/products` com `HTTP 200`, idêntico ao comportamento do Laravel.

- **Select Related (JOIN):** A listagem de produtos utiliza `select_related('categoria')`, equivalente ao `with('categoria')` do Eloquent, evitando o problema de N+1 queries para tornar a comparação de desempenho com o Laravel mais precisa.

- **`JSONRenderer` exclusivo:** A *Browsable API* (interface HTML) do DRF foi desabilitada via `DEFAULT_RENDERER_CLASSES`. A API retorna apenas JSON puro em qualquer contexto, comportamento idêntico ao Laravel com o middleware `ForceJsonResponse`.

- **Connection Pooling via PgBouncer:** A infraestrutura Docker inclui um contêiner PgBouncer (porta `6433`). Os testes são executados em dois cenários: conectando diretamente ao PostgreSQL (porta `5432`) e via PgBouncer, variando apenas a variável `DATABASE_HOST` no `.env`.

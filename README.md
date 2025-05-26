# technical-octo-friend
RESTful FastAPI Lu Estilo (Integração com Whatsapp)

## Pré requisitos:

- Docker
- Docker Compose

## 1. Como rodar:

#### Subir os containeres:

```
docker-compose up -d --build
```

Isso vai subir os serviços.

#### Ver os logs (opcional):
```
docker-compose logs -f
```

#### Acessar a aplicação:
Acesse `http://localhost:8000` no seu navegador.

### Rodar os testes com Docker Compose:
```
docker-compose run -rm test
```

### Parando o Projeto:
```
docker-compose down
```
  - Para limpar os dados persistentes pare o projeto com:
    ```
    docker-compose down -v
    ```

## 2. Endpoints:

### a. Autenticação:
- [x] i. POST /auth/login: Autenticação de usuário.
- [x] ii. POST /auth/register: Registro de novo usuário.
- [x] iii. POST /auth/refresh-token: Refresh de token JWT.

### b. Clientes:
- [x] i. GET /clients: Listar todos os clientes, com suporte a
paginação e filtro por nome e email.
- [x] ii. POST /clients: Criar um novo cliente, validando email e CPF
únicos.
- [x] iii. GET /clients/{id}: Obter informações de um cliente
específico.
- [x] iv. PUT /clients/{id}: Atualizar informações de um cliente
específico.
- [x] v. DELETE /clients/{id}: Excluir um cliente.

### c. Produtos:
- [x] i. GET /products: Listar todos os produtos, com suporte a
paginação e filtros por categoria, preço e disponibilidade.
- [x] ii. POST /products: Criar um novo produto, contendo os
seguintes atributos: descrição, valor de venda, código de
barras, seção, estoque inicial, e data de validade (quando
aplicável) e imagens.
- [x] iii. GET /products/{id}: Obter informações de um produto
específico.
- [x] iv. PUT /products/{id}: Atualizar informações de um produto
específico.
- [x] v. DELETE /products/{id}: Excluir um produto.

### d. Pedidos:
- [x] i. GET /orders: Listar todos os pedidos, incluindo os seguintes
filtros: período, seção dos produtos, id_pedido, status do
pedido e cliente.
- [x] ii. POST /orders: Criar um novo pedido contendo múltiplos
produtos, validando estoque disponível.
- [x] iii. GET /orders/{id}: Obter informações de um pedido
específico.
- [x] iv. PUT /orders/{id}: Atualizar informações de um pedido
específico, incluindo status do pedido.
- [x] v. DELETE /orders/{id}: Excluir um pedido.

## 3. Autenticação e Autorização:
- [x] a. Utilize JWT (JSON Web Token) para autenticação.
- [x] b. Proteja as rotas de clientes, produtos e pedidos para que apenas
usuários autenticados possam acessá-las.
- [x] c. Implemente níveis de acesso: admin e usuário regular, restringindo
ações específicas a cada nível.

## 4. Validação e Tratamento de Erros:
- [x] a. Implemente validações adequadas para todos os endpoints.
- [x] b. Garanta que respostas de erro sejam informativas e sigam um
padrão consistente.
- [ ] c. Registre erros críticos em um sistema de monitoramento, como
Sentry.

## 5. Banco de Dados:
- [x] a. Utilize um banco de dados relacional como PostgreSQL.
- [x] b. Implemente migrações de banco de dados para facilitar a
configuração do ambiente.
- [x] c. Utilize índices adequados para melhorar a performance das
consultas.

## 6. Documentação da API:
- [x] a. Utilize o sistema de documentação automática do FastAPI
(Swagger).
- [ ] b. Inclua exemplos de requisições e respostas para cada endpoint.
- [ ] c. Adicione seções de descrição detalhada para cada endpoint,
explicando regras de negócio e casos de uso.

## 7. Testes:
- [x] a. Implemente testes unitários e de integração.
- [ ] a. Implemente testes de integração.
- [x] b. Utilize pytest para os testes.

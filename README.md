# technical-octo-friend
RESTful FastAPI Lu Estilo (Integração com Whatsapp)


## 2. Endpoints:

### a. Autenticação:
- [ ] i. POST /auth/login: Autenticação de usuário.
- [ ] ii. POST /auth/register: Registro de novo usuário.
- [ ] iii. POST /auth/refresh-token: Refresh de token JWT.

### b. Clientes:
- [ ] i. GET /clients: Listar todos os clientes, com suporte a
paginação e filtro por nome e email.
- [ ] ii. POST /clients: Criar um novo cliente, validando email e CPF
únicos.
- [ ] iii. GET /clients/{id}: Obter informações de um cliente
específico.
- [ ] iv. PUT /clients/{id}: Atualizar informações de um cliente
específico.
- [ ] v. DELETE /clients/{id}: Excluir um cliente.

### c. Produtos:
- [ ] i. GET /products: Listar todos os produtos, com suporte a
paginação e filtros por categoria, preço e disponibilidade.
- [ ] ii. POST /products: Criar um novo produto, contendo os
seguintes atributos: descrição, valor de venda, código de
barras, seção, estoque inicial, e data de validade (quando
aplicável) e imagens.
- [ ] iii. GET /products/{id}: Obter informações de um produto
específico.
- [ ] iv. PUT /products/{id}: Atualizar informações de um produto
específico.
- [ ] v. DELETE /products/{id}: Excluir um produto.

### d. Pedidos:
- [ ] i. GET /orders: Listar todos os pedidos, incluindo os seguintes
filtros: período, seção dos produtos, id_pedido, status do
pedido e cliente.
- [ ] ii. POST /orders: Criar um novo pedido contendo múltiplos
produtos, validando estoque disponível.
- [ ] iii. GET /orders/{id}: Obter informações de um pedido
específico.
- [ ] iv. PUT /orders/{id}: Atualizar informações de um pedido
específico, incluindo status do pedido.
- [ ] v. DELETE /orders/{id}: Excluir um pedido.

## 3. Autenticação e Autorização:
- [ ] a. Utilize JWT (JSON Web Token) para autenticação.
- [ ] b. Proteja as rotas de clientes, produtos e pedidos para que apenas
usuários autenticados possam acessá-las.
- [ ] c. Implemente níveis de acesso: admin e usuário regular, restringindo
ações específicas a cada nível.

## 4. Validação e Tratamento de Erros:
- [ ] a. Implemente validações adequadas para todos os endpoints.
- [ ] b. Garanta que respostas de erro sejam informativas e sigam um
padrão consistente.
- [ ] c. Registre erros críticos em um sistema de monitoramento, como
Sentry.

## 5. Banco de Dados:
- [ ] a. Utilize um banco de dados relacional como PostgreSQL.
- [ ] b. Implemente migrações de banco de dados para facilitar a
configuração do ambiente.
- [ ] c. Utilize índices adequados para melhorar a performance das
consultas.

## 6. Documentação da API:
- [ ] a. Utilize o sistema de documentação automática do FastAPI
(Swagger).
- [ ] b. Inclua exemplos de requisições e respostas para cada endpoint.
- [ ] c. Adicione seções de descrição detalhada para cada endpoint,
explicando regras de negócio e casos de uso.

## 7. Testes:
- [ ] a. Implemente testes unitários e de integração.
- [ ] b. Utilize pytest para os testes.

# technical-octo-friend
RESTful FastAPI Lu Estilo (Integração com Whatsapp)


## 2. Endpoints:

### a. Autenticação:
- [x] i. POST /auth/login: Autenticação de usuário.
- [x] ii. POST /auth/register: Registro de novo usuário.
- [ ] iii. POST /auth/refresh-token: Refresh de token JWT.

### b. Clientes:

paginação e filtro por nome e email.
  - trocar responses

### c. Produtos:

### d. Pedidos:


## 3. Autenticação e Autorização:

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
## 6. Documentação da API:

- [ ] b. Inclua exemplos de requisições e respostas para cada endpoint.
- [ ] c. Adicione seções de descrição detalhada para cada endpoint,
explicando regras de negócio e casos de uso.

## 7. Testes:
- [ ] a. Implemente testes unitários e de integração.
- [ ] b. Utilize pytest para os testes.

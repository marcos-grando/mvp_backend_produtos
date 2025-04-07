### Desenvolvimento Full Stack - PUC-Rio

## MVP Back End com Flask + Interface React:
# Big Loja (loja virtual) 🛒

O objetivo do MVP foi desenvolver uma loja virtual, contemplando tanto a experiência do usuário quanto o gerenciamento administrativo do sistema.
👤 Usuário: pode navegar entre produtos, filtrar por categoria ou preço, adicionar e manipular itens no carrinho, finalizar compras e acompanhar pedidos no histórico.
🛠️ Administrador: conta com um painel de controle que permite o cadastro e gerenciamento de produtos e categorias, além de visualizar todos os pedidos realizados (incluindo a opção de cancelamento de pedidos).

---

## 📦 API de Produtos (backend_produtos)

Esse repositório é o backend que cuida do cadastro, edição, listagem e remoção de produtos da loja virtual. Ele também é responsável por fazer upload das imagens dos produtos. Tudo é feito com Flask, e o container é gerenciado pelo Docker.

---

## 🚀 O que essa API faz

- 🔍 **Listar produtos** com filtros por categoria e valor
- ➕ **Cadastrar novos produtos**, com upload de imagem
- ✏️ **Editar produtos existentes**
- ❌ **Remover produtos**
- 📤 **Upload de imagem** (imagem de produto via rota separada)
- 🔁 **Reabastecer estoque** de todos os produtos

---

## 🧪 `populate_db.py`

- Este repositório inclui também o `populate_db.py`, que consome a API externa FakeStore para popular a base de dados com produtos de exemplo.

---

## 🔄 Principais rotas

| Método | Rota                      | Função                                  |
|--------|---------------------------|-----------------------------------------|
| GET    | `/produtos`               | Lista todos os produtos                 |
| POST   | `/produtos`               | Cadastra um novo produto                |
| GET    | `/produtos/<id>`          | Retorna um produto específico           |
| PUT    | `/produtos/<id>`          | Atualiza um produto                     |
| DELETE | `/produtos/<id>`          | Remove um produto                       |
| POST   | `/upload-imagem`          | Faz o upload de uma imagem              |
| POST   | `/reabastecer`            | Reabastece o estoque de todos os produtos |

---

## 🛠️ Tecnologias utilizadas

- **Python 3.10**
- **Flask** com `flask_sqlalchemy` e `flask_cors`
- **Werkzeug** para tratamento de uploads
- **uuid**, **datetime**, **zoneinfo** e **os** para geração de IDs, datas e manipulação de arquivos
- **Docker** para containerização

---

## 📦 Como rodar o projeto

Esse container faz parte de um sistema completo e depende dos seguintes repositórios para funcionar corretamente:

### Estrutura do sistema:

- 🌐 **API externa**: [FakeStore](https://fakestoreapi.com/) → usada para popular a base com produtos fictícios. O modelo `Produto` foi estruturado com base nos dados dessa API (nome, valor, imagem, etc).
- 🔹 [`backend_categorias`](https://github.com/seu-usuario/backend_categorias) → responsável pelo cadastro e gerenciamento das categorias dos produtos
- 🔹 [`backend_produtos`] ← Você está nesse repositório
- 🔹 [`backend_compras`](https://github.com/seu-usuario/backend_compras) → responsável por registrar e consultar compras feitas na loja
- 🔸 [`backend_shared`](https://github.com/seu-usuario/backend_shared) → módulo auxiliar compartilhado (banco de dados, pastas de upload, etc)
- 💠 [`frontend`](https://github.com/seu-usuario/frontend) → interface React responsável pela exibição dos produtos, carrinho, compras e painel administrativo, conectando-se às APIs

**Esse container precisa acessar um volume compartilhado (`backend_shared`) para acessar:**
 - O banco de dados SQLite
 - A pasta `uploads/` (salvando a cópia da imagem recebida)
 - Configuração centralizada da aplicação Flask em `config.py`

***OBS: `docker-compose`***  
 - O sistema utiliza 3 APIs diferentes, com dependências entre os módulos  
 - Por isso, é recomendado utilizar o `docker-compose`, que está no repositório `frontend`  
 - Isso evita a necessidade de buildar e subir manualmente cada componente um por um

---

## ▶️ Como rodar

1. Clone esse repositório  
2. Certifique-se de que os outros containers do sistema estão presentes na mesma estrutura  
3. No terminal, execute:

```bash
docker-compose up --build -d
```

---

## 🧠 Observações
Esse repositório faz parte de um MVP acadêmico. O sistema foi dividido em partes que se comunicam entre si por rotas. O backend foi feito com Flask (Python) e frontend com React.js.

### 🙋‍♂️ Autor
Desenvolvido por Marcos Grando ✌️

"""
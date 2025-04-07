import requests
from flask import Flask
from shared.config import configure_app
from models import db, Produto, Categoria

app = Flask(__name__)
configure_app(app)
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # criando as categorias traduzidas
    categorias = {
        "electronics": "Eletrônicos",
        "jewelery": "Jóias",
        "men's clothing": "Roupas Masculinas",
        "women's clothing": "Roupas Femininas"
    }
    for slug, nome in categorias.items():
        if not Categoria.query.filter_by(nome=nome).first():
            db.session.add(Categoria(nome=nome))
    db.session.commit()

    # buscando os produts da api fake store
    resposta = requests.get("https://fakestoreapi.com/products")
    if resposta.status_code == 200:
        produtos_api = resposta.json()

        for produto in produtos_api:
            categoria_nome = categorias.get(produto["category"].lower(), "Outros")
            categoria = Categoria.query.filter_by(nome=categoria_nome).first()

            if categoria and not Produto.query.filter_by(nome=produto["title"]).first():
                novo_produto = Produto(
                    nome=produto["title"],
                    valor=produto["price"],
                    categoria_id=categoria.id,
                    estoque=100,
                    imagem=produto["image"]
                )
                db.session.add(novo_produto)

    db.session.commit()
    print("Banco de dados recriado e populado com sucesso!")

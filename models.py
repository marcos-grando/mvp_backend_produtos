from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    estoque = db.Column(db.Integer, default=100)
    imagem = db.Column(db.String(255), nullable=True)

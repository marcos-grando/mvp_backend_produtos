from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from shared.config import configure_app
from models import db, Produto, Categoria
from werkzeug.utils import secure_filename
import os
import requests
import uuid

app = Flask(__name__)
configure_app(app)
db.init_app(app)
CORS(app)


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/uploads/<path:filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload-imagem", methods=["POST"])
def upload_imagem():

    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhuma imagem foi enviada"}), 400

    imagem = request.files["imagem"]

    if imagem.filename == "":
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    if not allowed_file(imagem.filename):
        return jsonify({"erro": "Extensão de arquivo não permitida"}), 400

    filename = f"{uuid.uuid4().hex}_{secure_filename(imagem.filename)}"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        imagem.save(filepath)
    except Exception as e:
        return jsonify({"erro": "Erro ao salvar imagem"}), 500

    url_imagem = f"/uploads/{filename}"
    return jsonify({"url": url_imagem}), 200


# C - Adciona novos produtos
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    dados = request.form
    imagem = request.files.get("imagem")
    url_imagem = "uploads/img_null.jpg"

    categoria = Categoria.query.filter_by(nome=dados.get("categoria")).first()
    if not categoria:
        nova_categoria = Categoria(nome=dados["categoria"])
        db.session.add(nova_categoria)
        db.session.commit()
        categoria = nova_categoria

    if imagem:
        resposta = requests.post(
            "http://localhost:5000/upload-imagem",
            files={"imagem": (imagem.filename, imagem, imagem.content_type)}
        )
        if resposta.status_code == 200:
            url_imagem = resposta.json().get("url", url_imagem)

    novo_produto = Produto(
        nome=dados["nome"],
        valor=dados["valor"],
        categoria_id=categoria.id,
        estoque=dados.get("estoque", 100),
        imagem=url_imagem
    )

    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({"mensagem": "Novo produto adicionado com sucesso!", "imagem_url": url_imagem}), 201

# R - Mostra todos produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    categorias_param = request.args.get("categorias")
    ordenar_valor = request.args.get("valor")
    query = Produto.query

    if categorias_param:
        categorias_lista = [c.lower().strip() for c in categorias_param.split(",")]
        query = query.join(Categoria).filter(Categoria.nome.in_(categorias_lista))

    if ordenar_valor == "asc":
        query = query.order_by(Produto.valor.asc())
    elif ordenar_valor == "desc":
        query = query.order_by(Produto.valor.desc())

    produtos = query.all()

    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "valor": p.valor,
            "estoque": p.estoque,
            "categoria_id": p.categoria.id if p.categoria else None,
            "categoria": p.categoria.nome if p.categoria else "Desconhecida",
            "imagem": p.imagem if p.imagem.startswith("http") else f"http://localhost:5001/{p.imagem}"
        }
        for p in produtos
    ])

# U - Atualizar info do produto
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.form
    imagem = request.files.get("imagem")

    if 'nome' in dados and dados['nome'].strip():
        produto.nome = dados['nome']

    if 'valor' in dados and dados['valor'].strip():
        try:
            produto.valor = float(dados['valor'])
        except ValueError:
            return jsonify({"erro": "Valor inválido"}), 400

    if 'estoque' in dados and dados['estoque'].strip():
        try:
            produto.estoque = int(dados['estoque'])
        except ValueError:
            return jsonify({"erro": "Estoque inválido"}), 400

    if 'categoria' in dados and dados['categoria'].strip():
        categoria = Categoria.query.get(dados['categoria'])
        if not categoria:
            return jsonify({"erro": "Categoria inválida"}), 400
        produto.categoria_id = categoria.id

    if imagem:
        if produto.imagem and "img_null.jpg" not in produto.imagem:
            nome_arquivo_antigo = os.path.basename(produto.imagem)
            caminho_antigo = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo_antigo)
            if os.path.exists(caminho_antigo):
                os.remove(caminho_antigo)

        resposta = requests.post(
            "http://localhost:5000/upload-imagem",
            files={"imagem": (imagem.filename, imagem, imagem.content_type)}
        )

        if resposta.status_code == 200:
            produto.imagem = resposta.json().get("url")
        else:
            return jsonify({"erro": "Falha no upload da imagem"}), 500

    db.session.commit()
    return jsonify({"mensagem": "O produto foi atualizado!"})

# D - Remover produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    if produto.imagem and "img_null.jpg" not in produto.imagem:
        caminho_imagem = os.path.join(app.config["UPLOAD_FOLDER"], os.path.basename(produto.imagem))
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)

    db.session.delete(produto)
    db.session.commit()

    return jsonify({"mensagem": "Produto removido com sucesso!"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

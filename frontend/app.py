from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro de produtos
@app.route('/cadastro', methods=['GET'])
def exibir_formulario_produto():
    return render_template('cadastro.html')

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    nome = request.form['nome']
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    payload = {
        'nome': nome,
        'categoria': categoria,
        'quantidade': quantidade,
        'preco': preco
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/estoque/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('listar_estoque'))
    else:
        return "Erro ao adicionar produto", 500

# Rota para listar todos os produtos
@app.route('/estoque', methods=['GET'])
def listar_estoque():
    response = requests.get(f'{API_BASE_URL}/api/v1/estoque/')
    try:
        produtos = response.json()
    except:
        produtos = []
    return render_template('estoque.html', produtos=produtos)

# Rota para exibir o formulário de atualização de produto
@app.route('/atualizar/<int:produto_id>', methods=['GET'])
def exibir_formulario_atualizacao(produto_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/estoque/{produto_id}")
    if response.status_code == 404:
        return "Produto não encontrado", 404
    produto = response.json()
    return render_template('atualizar.html', produto=produto)

# Rota para enviar os dados de atualização para a API
@app.route('/atualizar/<int:produto_id>', methods=['POST'])
def atualizar_produto(produto_id):
    nome = request.form.get('nome')
    categoria = request.form.get('categoria')
    quantidade = request.form.get('quantidade')
    preco = request.form.get('preco')

    payload = {
        'nome': nome,
        'categoria': categoria,
        'quantidade': quantidade,
        'preco': preco
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/estoque/{produto_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_estoque'))
    else:
        return "Erro ao atualizar produto", 500

# Rota para exibir o formulário de venda de produto
@app.route('/vender/<int:produto_id>', methods=['GET'])
def exibir_formulario_venda(produto_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/estoque/{produto_id}")
    if response.status_code == 404:
        return "Produto não encontrado", 404
    produto = response.json()
    return render_template('vender.html', produto=produto)

# Rota para registrar a venda de um produto
@app.route('/vender/<int:produto_id>', methods=['POST'])
def vender_produto(produto_id):
    quantidade = request.form['quantidade']

    payload = {
        'quantidade': quantidade
    }

    response = requests.put(f"{API_BASE_URL}/api/v1/estoque/{produto_id}/vender/", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_estoque'))
    else:
        return "Erro ao vender produto", 500

# Rota para listar todas as vendas
@app.route('/vendas', methods=['GET'])
def listar_vendas():
    response = requests.get(f"{API_BASE_URL}/api/v1/vendas/")
    try:
        vendas = response.json()
    except:
        vendas = []
    total_vendas = sum(venda['valor_venda'] for venda in vendas)
    return render_template('vendas.html', vendas=vendas, total_vendas=total_vendas)

# Rota para excluir um produto
@app.route('/excluir/<int:produto_id>', methods=['POST'])
def excluir_produto(produto_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/estoque/{produto_id}")
    
    if response.status_code == 200:
        return redirect(url_for('listar_estoque'))
    else:
        return "Erro ao excluir produto", 500

# Rota para resetar o banco de dados
@app.route('/resetar-banco', methods=['GET'])
def resetar_banco():
    response = requests.delete(f"{API_BASE_URL}/api/v1/estoque/")
    
    if response.status_code == 200:
        return render_template('confirmacao.html')
    else:
        return "Erro ao resetar banco de dados", 500


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')

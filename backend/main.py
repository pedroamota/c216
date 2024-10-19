from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
from db.database import DatabaseConnection
import os

app = FastAPI()

class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    quantidade: int
    #dataValidade: int
    preco: float

class Produto(ProdutoBase):
    id: Optional[int] = None

class VendaProduto(BaseModel):
    quantidade: int

class AtualizarProduto(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[str] = None
    quantidade: Optional[int] = None
    #dataValidade: Optional[datetime] = None
    preco: Optional[float] = None

# Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

async def produto_existe(nome: str, categoria: str, conn):
    query = "SELECT 1 FROM estoque WHERE LOWER(nome) = LOWER($1) AND LOWER(categoria) = LOWER($2)"
    return await conn.fetchval(query, nome, categoria)

# Buscar um produto por ID
async def buscar_produto_por_id(produto_id: int, conn):
    query = "SELECT * FROM estoque WHERE id = $1"
    produto = await conn.fetchrow(query, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto

# 1. Adicionar um novo produto
@app.post("/api/v1/estoque/", status_code=201)
async def adicionar_produto(produto: ProdutoBase):
    async with DatabaseConnection() as conn:
        if await produto_existe(produto.nome, produto.categoria, conn):
            raise HTTPException(status_code=400, detail="Produto já existe.")
        query = "INSERT INTO estoque (nome, categoria, quantidade, preco) VALUES ($1, $2, $3, $4)"
        await conn.execute(query, produto.nome, produto.categoria, produto.quantidade, produto.preco)
        return {"message": "Produto adicionado com sucesso!"}

# 2. Listar todos os produtos no estoque
@app.get("/api/v1/estoque/", response_model=List[Produto])
async def listar_estoque():
    async with DatabaseConnection() as conn:
        query = "SELECT * FROM estoque"
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

# 3. Buscar produto por ID
@app.get("/api/v1/estoque/{produto_id}")
async def listar_produto_por_id(produto_id: int):
    async with DatabaseConnection() as conn:
        produto = await buscar_produto_por_id(produto_id, conn)
        return dict(produto)

# 4. Vender um produto
@app.put("/api/v1/estoque/{produto_id}/vender/")
async def vender_produto(produto_id: int, venda: VendaProduto):
    async with DatabaseConnection() as conn:
        produto = await buscar_produto_por_id(produto_id, conn)

        if produto['quantidade'] < venda.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente no estoque.")

        nova_quantidade = produto['quantidade'] - venda.quantidade
        update_query = "UPDATE estoque SET quantidade = $1 WHERE id = $2"
        await conn.execute(update_query, nova_quantidade, produto_id)

        valor_venda = produto['preco'] * venda.quantidade
        insert_venda_query = "INSERT INTO vendas (produto_id, quantidade_vendida, valor_venda) VALUES ($1, $2, $3)"
        await conn.execute(insert_venda_query, produto_id, venda.quantidade, valor_venda)

        produto_atualizado = dict(produto)
        produto_atualizado['quantidade'] = nova_quantidade
        return {"message": "Venda realizada com sucesso!", "produto": produto_atualizado}

# 5. Atualizar atributos
@app.patch("/api/v1/estoque/{produto_id}")
async def atualizar_produto(produto_id: int, produto_atualizacao: AtualizarProduto):
    async with DatabaseConnection() as conn:
        produto = await buscar_produto_por_id(produto_id, conn)

        update_query = """
            UPDATE estoque
            SET nome = COALESCE($1, nome),
                categoria = COALESCE($2, categoria),
                quantidade = COALESCE($3, quantidade),
                preco = COALESCE($4, preco)
            WHERE id = $5
        """
        await conn.execute(
            update_query,
            produto_atualizacao.nome,
            produto_atualizacao.categoria,
            produto_atualizacao.quantidade,
            produto_atualizacao.preco,
            produto_id
        )
        return {"message": "Produto atualizado com sucesso!"}

# 6. Remover um produto
@app.delete("/api/v1/estoque/{produto_id}")
async def remover_produto(produto_id: int):
    async with DatabaseConnection() as conn:
        produto = await buscar_produto_por_id(produto_id, conn)

        delete_query = "DELETE FROM estoque WHERE id = $1"
        await conn.execute(delete_query, produto_id)
        return {"message": "Produto removido com sucesso!"}

# 7. Resetar banco de dados de estoque
@app.delete("/api/v1/estoque/")
async def resetar_estoque():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    async with DatabaseConnection() as conn:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}

# 8. Listar vendas
@app.get("/api/v1/vendas/")
async def listar_vendas():
    async with DatabaseConnection() as conn:
        query = "SELECT * FROM vendas"
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

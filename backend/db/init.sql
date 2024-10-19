DROP TABLE IF EXISTS "vendas";
DROP TABLE IF EXISTS "estoque";

CREATE TABLE "estoque" (
    "id" SERIAL PRIMARY KEY,
    "nome" VARCHAR(255) NOT NULL,
    "categoria" VARCHAR(255) NOT NULL,
    "quantidade" INTEGER NOT NULL,
    "preco" FLOAT NOT NULL
);

CREATE TABLE "vendas" (
    "id" SERIAL PRIMARY KEY,
    "produto_id" INTEGER REFERENCES estoque(id) ON DELETE CASCADE,
    "quantidade_vendida" INTEGER NOT NULL,
    "valor_venda" FLOAT NOT NULL,
    "data_venda" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "estoque" ("nome", "categoria", "quantidade", "preco") VALUES ('Azeite', 'Óleos e Temperos', 10, 150.00);
INSERT INTO "estoque" ("nome", "categoria", "quantidade", "preco") VALUES ('Escova de dente', 'Higiente', 5, 30.00);
INSERT INTO "estoque" ("nome", "categoria", "quantidade", "preco") VALUES ('Feijão', 'Grãos e Cereais', 15, 10.00)
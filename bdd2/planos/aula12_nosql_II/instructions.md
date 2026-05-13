# Aula 12 — MongoDB na Prática

## Objetivo

Nesta aula você vai carregar uma base simples de e-commerce no MongoDB e praticar:

- consultas com `find`;
- filtros com operadores;
- projeções;
- atualizações;
- índices;
- aggregation pipeline.

## Pré-requisitos

Instale antes da aula:

- MongoDB Community Server;
- MongoDB Shell (`mongosh`).

## Instalação no Windows

Instale primeiro o servidor:

1. Acesse `https://www.mongodb.com/try/download/community`.
2. Escolha `Version 8.0`.
3. Em `Platform`, escolha `Windows`.
4. Em `Package`, escolha `msi`.
5. Baixe e execute o instalador.
6. Use a instalação `Complete`.
7. Marque `Install MongoD as a Service`.
8. Finalize a instalação.

Instale depois o shell:

1. Acesse `https://www.mongodb.com/try/download/shell`.
2. Escolha `Windows 64-bit MSI`.
3. Baixe e execute o instalador.
4. Se aparecer a opção de adicionar ao `PATH`, deixe marcada.
5. Abra um novo terminal depois da instalação.

Confirme:

```powershell
mongosh --version
mongosh
```

## Instalação no Ubuntu 24.04 Noble

Use o repositório oficial da MongoDB:

```bash
sudo apt-get install -y gnupg curl

curl -fsSL https://pgp.mongodb.com/server-8.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
  --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

sudo apt-get update
sudo apt-get install -y mongodb-org mongodb-mongosh
```

Inicie e habilite o serviço:

```bash
sudo systemctl start mongod
sudo systemctl status mongod
sudo systemctl enable mongod
```

Se o serviço ainda não aparecer, rode:

```bash
sudo systemctl daemon-reload
sudo systemctl start mongod
```

Depois da instalação, confirme no terminal:

```bash
mongosh --version
```

## Verificar se o servidor está rodando

Abra o shell:

```bash
mongosh
```

Execute:

```javascript
db.runCommand({ ping: 1 })
```

Se aparecer `ok: 1`, o servidor está respondendo.

## Carregar a base da aula

A partir da pasta `bdd2`, rode:

```bash
mongosh --file planos/aula12_nosql_II/seed.mongodb.js
```

O script deve mostrar:

```text
Base bdd2_aula12 carregada.
produtos: 10
clientes: 3
pedidos: 4
```

## Abrir a base

```bash
mongosh bdd2_aula12
```

Confira as coleções:

```javascript
show collections
db.produtos.countDocuments()
db.clientes.countDocuments()
db.pedidos.countDocuments()
```

## Consultas básicas

```javascript
db.produtos.find()

db.produtos.find({ categoria: "notebook" })

db.produtos.find(
  { categoria: "notebook" },
  { nome: 1, preco: 1, estoque: 1 }
)
```

## Filtros com operadores

```javascript
db.produtos.find({
  preco: { $gte: 1000, $lte: 6000 }
})

db.produtos.find({
  categoria: { $in: ["notebook", "celular"] }
})

db.produtos.find({
  $or: [
    { estoque: { $lt: 10 } },
    { tags: "promocao" }
  ]
})
```

## Campos aninhados e arrays

```javascript
db.produtos.find({
  "specs.ram_gb": { $gte: 16 }
})

db.produtos.find({
  "specs.camera_mp": { $gte: 48 }
})

db.produtos.find({ tags: "promocao" })

db.produtos.find({
  tags: { $all: ["trabalho", "portatil"] }
})
```

## Atualizações

```javascript
db.produtos.updateOne(
  { sku: "NB-001" },
  { $set: { preco: 4999.9 } }
)

db.produtos.updateOne(
  { sku: "NB-001" },
  { $inc: { estoque: -1 } }
)

db.produtos.updateOne(
  { sku: "NB-001" },
  { $push: { tags: "oferta-relampago" } }
)
```

Confira o resultado:

```javascript
db.produtos.findOne(
  { sku: "NB-001" },
  { nome: 1, preco: 1, estoque: 1, tags: 1 }
)
```

## Índices

```javascript
db.produtos.find({
  categoria: "notebook",
  preco: { $lte: 6000 }
}).explain("executionStats")

db.produtos.createIndex({
  categoria: 1,
  preco: 1
})

db.produtos.find({
  categoria: "notebook",
  preco: { $lte: 6000 }
}).explain("executionStats")
```

Procure por:

- `COLLSCAN`: varredura sequencial da coleção;
- `IXSCAN`: uso de índice.

## Aggregation pipeline

Preço médio por categoria:

```javascript
db.produtos.aggregate([
  { $match: { estoque: { $gt: 0 } } },
  {
    $group: {
      _id: "$categoria",
      total: { $sum: 1 },
      precoMedio: { $avg: "$preco" }
    }
  },
  { $sort: { precoMedio: -1 } }
])
```

Receita por produto vendido:

```javascript
db.pedidos.aggregate([
  { $unwind: "$itens" },
  {
    $group: {
      _id: "$itens.sku",
      unidades: { $sum: "$itens.qtd" },
      receita: { $sum: { $multiply: ["$itens.qtd", "$itens.preco_unit"] } }
    }
  },
  { $sort: { receita: -1 } }
])
```

## Exercício

Resolva no `mongosh`:

1. Liste notebooks com pelo menos 16 GB de RAM e preço abaixo de R$ 6.000.
2. Mostre apenas `nome`, `preco`, `specs.ram_gb` e `estoque`.
3. Reduza o estoque de um produto vendido em 1 unidade.
4. Crie um índice que ajude a primeira consulta.
5. Calcule a receita total por SKU usando aggregation.

## Recomeçar do zero

Se quiser restaurar os dados originais:

```bash
mongosh --file planos/aula12_nosql_II/seed.mongodb.js
```

use("bdd2_aula12");

db.produtos.drop();
db.clientes.drop();
db.pedidos.drop();

db.produtos.insertMany([
  {
    sku: "NB-001",
    nome: "Notebook Aurora 14",
    categoria: "notebook",
    preco: 5299.9,
    estoque: 18,
    specs: {
      processador: "Ryzen 7",
      ram_gb: 16,
      ssd_gb: 512,
      tela_polegadas: 14,
      peso_kg: 1.35
    },
    tags: ["trabalho", "portatil"]
  },
  {
    sku: "NB-002",
    nome: "Notebook Titan 16",
    categoria: "notebook",
    preco: 8799.9,
    estoque: 7,
    specs: {
      processador: "Core i9",
      ram_gb: 32,
      ssd_gb: 1024,
      tela_polegadas: 16,
      gpu: "RTX 4070"
    },
    tags: ["gamer", "performance"]
  },
  {
    sku: "NB-003",
    nome: "Notebook Campus 15",
    categoria: "notebook",
    preco: 3499.9,
    estoque: 31,
    specs: {
      processador: "Core i5",
      ram_gb: 8,
      ssd_gb: 256,
      tela_polegadas: 15.6
    },
    tags: ["estudo", "entrada"]
  },
  {
    sku: "NB-004",
    nome: "Notebook Studio 14",
    categoria: "notebook",
    preco: 5899.9,
    estoque: 12,
    specs: {
      processador: "Ryzen 7",
      ram_gb: 16,
      ssd_gb: 1024,
      tela_polegadas: 14.5
    },
    tags: ["trabalho", "promocao"]
  },
  {
    sku: "CL-001",
    nome: "Smartphone Prisma X",
    categoria: "celular",
    preco: 3199.9,
    estoque: 24,
    specs: {
      processador: "Snapdragon 8",
      ram_gb: 12,
      armazenamento_gb: 256,
      camera_mp: 50,
      tela_polegadas: 6.4,
      cinco_g: true
    },
    tags: ["android", "promocao"]
  },
  {
    sku: "CL-002",
    nome: "Smartphone Nuvem Mini",
    categoria: "celular",
    preco: 1899.9,
    estoque: 43,
    specs: {
      processador: "Dimensity 7200",
      ram_gb: 8,
      armazenamento_gb: 128,
      camera_mp: 48,
      tela_polegadas: 6.1,
      cinco_g: true
    },
    tags: ["android", "compacto"]
  },
  {
    sku: "LV-001",
    nome: "Sistemas de Banco de Dados",
    categoria: "livro",
    preco: 229.9,
    estoque: 11,
    specs: {
      autor: "Elmasri e Navathe",
      paginas: 808,
      idioma: "pt-BR",
      formato: "capa dura"
    },
    tags: ["database", "academico"]
  },
  {
    sku: "LV-002",
    nome: "Designing Data-Intensive Applications",
    categoria: "livro",
    preco: 279.9,
    estoque: 9,
    specs: {
      autor: "Martin Kleppmann",
      paginas: 616,
      idioma: "en",
      formato: "brochura"
    },
    tags: ["database", "arquitetura"]
  },
  {
    sku: "AC-001",
    nome: "Teclado Mecânico K2",
    categoria: "acessorio",
    preco: 389.9,
    estoque: 28,
    specs: {
      conexao: "Bluetooth",
      layout: "ABNT2",
      switch: "brown"
    },
    tags: ["escritorio", "promocao"]
  },
  {
    sku: "AC-002",
    nome: "Headset Focus USB",
    categoria: "acessorio",
    preco: 249.9,
    estoque: 0,
    specs: {
      conexao: "USB-C",
      microfone: true,
      cancelamento_ruido: true
    },
    tags: ["reuniao", "escritorio"]
  }
]);

db.clientes.insertMany([
  {
    codigo: "CLI-001",
    nome: "Ana Silva",
    email: "ana@example.com",
    perfil: {
      cidade: "Curitiba",
      tipo: "pessoa_fisica"
    }
  },
  {
    codigo: "CLI-002",
    nome: "Bruno Costa",
    email: "bruno@example.com",
    perfil: {
      cidade: "São Paulo",
      tipo: "pessoa_fisica"
    }
  },
  {
    codigo: "CLI-003",
    nome: "Dados & Cia",
    email: "compras@dadosecia.example",
    perfil: {
      cidade: "Belo Horizonte",
      tipo: "empresa"
    }
  }
]);

db.pedidos.insertMany([
  {
    numero: "PED-1001",
    cliente_codigo: "CLI-001",
    criado_em: ISODate("2026-05-01T10:30:00Z"),
    status: "pago",
    itens: [
      { sku: "NB-001", qtd: 1, preco_unit: 5299.9 },
      { sku: "AC-001", qtd: 1, preco_unit: 389.9 }
    ]
  },
  {
    numero: "PED-1002",
    cliente_codigo: "CLI-002",
    criado_em: ISODate("2026-05-02T14:10:00Z"),
    status: "pago",
    itens: [
      { sku: "CL-001", qtd: 1, preco_unit: 3199.9 },
      { sku: "AC-002", qtd: 1, preco_unit: 249.9 }
    ]
  },
  {
    numero: "PED-1003",
    cliente_codigo: "CLI-003",
    criado_em: ISODate("2026-05-04T09:45:00Z"),
    status: "enviado",
    itens: [
      { sku: "NB-004", qtd: 3, preco_unit: 5899.9 },
      { sku: "AC-001", qtd: 3, preco_unit: 379.9 },
      { sku: "LV-002", qtd: 2, preco_unit: 279.9 }
    ]
  },
  {
    numero: "PED-1004",
    cliente_codigo: "CLI-001",
    criado_em: ISODate("2026-05-06T18:20:00Z"),
    status: "aberto",
    itens: [
      { sku: "LV-001", qtd: 1, preco_unit: 229.9 },
      { sku: "LV-002", qtd: 1, preco_unit: 279.9 }
    ]
  }
]);

db.produtos.createIndex({ sku: 1 }, { unique: true });
db.clientes.createIndex({ codigo: 1 }, { unique: true });
db.pedidos.createIndex({ numero: 1 }, { unique: true });

print("Base bdd2_aula12 carregada.");
print("produtos: " + db.produtos.countDocuments());
print("clientes: " + db.clientes.countDocuments());
print("pedidos: " + db.pedidos.countDocuments());

// Script de inicialização do MongoDB
db = db.getSiblingDB("web-scraper-uniser");

// Criar usuário para a aplicação
db.createUser({
  user: "webscraper",
  pwd: "webscraper123",
  roles: [
    {
      role: "readWrite",
      db: "web-scraper-uniser",
    },
  ],
});

// Criar coleções iniciais
db.createCollection("researchers-data");
db.createCollection("search-history");

// Inserir dados de exemplo (opcional)
db["researchers-data"].insertOne({
  query: "exemplo",
  timestamp: new Date(),
  researcher_info: {
    name: "Exemplo de Pesquisador",
    institution: "Universidade Exemplo",
    h_index: 10,
    i10_index: 5,
    total_citations: 250,
  },
  platforms_data: {
    scholar: {
      found: true,
      publications_count: 15,
    },
  },
});

print("MongoDB inicializado com sucesso para Web Scraper UniSER");

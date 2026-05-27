from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "ifsp1234")

driver = GraphDatabase.driver(URI, auth=AUTH)
try:
    driver.verify_connectivity()
    print("Connected to Neo4j database")
except Exception:
    print("Failed to connect to Neo4j database")
    driver.close()
    raise SystemExit(1)

with driver.session() as session:
    session.run("match (n) detach delete n")
    session.run("""CREATE (p:Person {name: 'Keanu Reeves'})-[:ACTED_AS]->(c:Character {name: 'Neo'})-[:ACTED_IN]->(m:Movie {title: 'The Matrix'})""")
    session.run("""
CREATE (carrie:Person {name: 'Carrie-Anne Moss'})-[:ACTED_AS]->(trinity:Character {name: 'Trinity'}) 
WITH trinity
MATCH (m:Movie {title: 'The Matrix'})
MERGE (trinity)-[:ACTED_IN]->(m)
""")

    res = session.run("""
MATCH (p:Person)-[:ACTED_AS]->(c:Character)-[:ACTED_IN]->(m:Movie)
RETURN p.name AS actor, c.name AS character, m.title AS movie
""").data()

    for row in res:
        print(row)

driver.close()

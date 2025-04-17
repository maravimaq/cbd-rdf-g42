from rdflib import Graph, Namespace

g = Graph()
g.parse("data/monuments.ttl", format="ttl")
EX = Namespace("http://example.org/monuments#")


print("\n Distintos países:")
q1 = '''
SELECT DISTINCT ?country WHERE {
  ?m a ex:Monument ;
     ex:country ?country .
}
'''
for row in g.query(q1, initNs={"ex": EX}):
    print(f"- {row.country}")

print("\nMonumentos y sus arquitectos:")
q2 = """
PREFIX ex: <http://example.org/monuments#>
SELECT ?name ?architect WHERE {
  ?m a ex:Monument ;
     ex:name ?name ;
     ex:hasArchitect ?architect .
}
"""
for row in g.query(q2, initNs={"ex": EX}):
    print(f"- {row.name} (Architect: {row.architect})")

print("\nMonumentos con estilo arquitectónico:")
q3 = """
PREFIX ex: <http://example.org/monuments#>
SELECT ?name ?style WHERE {
  ?m a ex:Monument ;
     ex:name ?name ;
     ex:architecturalStyle ?style .
}
"""
for row in g.query(q3, initNs={"ex": EX}):
    print(f"- {row.name} (Style: {row.style})")

print("\n Monumentos en Asia:")
q4 = '''
SELECT ?name WHERE {
  ?m a ex:Monument ;
     ex:name ?name ;
     ex:continent "Asia" .
}
'''
for row in g.query(q4, initNs={"ex": EX}):
    print(f"- {row.name}")

print("\n Monumentos creados antes del año 1000:")
q5 = '''
SELECT ?name ?year WHERE {
  ?m a ex:Monument ;
     ex:name ?name ;
     ex:creationYear ?year .
  FILTER (xsd:integer(SUBSTR(STR(?year), 1, 4)) < 1000)
}
'''
for row in g.query(q5, initNs={"ex": EX, "xsd": Namespace("http://www.w3.org/2001/XMLSchema#")}):
    print(f"- {row.name} ({row.year})")

print("\n Monumentos de tipo 'public art':")
q6 = '''
SELECT ?name WHERE {
  ?m a ex:Monument ;
     ex:name ?name ;
     ex:type ?type .
  FILTER CONTAINS(LCASE(STR(?type)), "public art")
}
'''
for row in g.query(q6, initNs={"ex": EX}):
    print(f"- {row.name}")

print("\n Monumentos agrupados por país:")
q7 = '''
SELECT ?country (COUNT(?m) AS ?total) WHERE {
  ?m a ex:Monument ;
     ex:country ?country .
}
GROUP BY ?country
ORDER BY DESC(?total)
'''
for row in g.query(q7, initNs={"ex": EX}):
    print(f"- {row.country}: {row.total} monumentos")


print("\n Monumentos sin estilo asignado:")
q8 = '''
SELECT ?name WHERE {
  ?m a ex:Monument ;
     ex:name ?name .
  FILTER NOT EXISTS { ?m ex:hasStyle ?style }
}
'''
for row in g.query(q8, initNs={"ex": EX}):
    print(f"- {row.name}")

print("\n Monumentos con nombres que contienen 'temple':")
q9 = '''
SELECT ?name WHERE {
  ?m a ex:Monument ;
     ex:name ?name .
  FILTER CONTAINS(LCASE(?name), "temple")
}
'''
for row in g.query(q9, initNs={"ex": EX}):
    print(f"- {row.name}")

print("\n Monumentos por arquitecto:")
q10 = '''
SELECT ?architect (COUNT(?m) AS ?total) WHERE {
  ?m a ex:Monument ;
     ex:hasArchitect ?architect .
}
GROUP BY ?architect
ORDER BY DESC(?total)
'''
for row in g.query(q10, initNs={"ex": EX}):
    print(f"- {row.architect}: {row.total} monumentos")


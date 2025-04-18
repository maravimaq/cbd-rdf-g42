from rdflib import Graph, Namespace
from rdflib.namespace import XSD

g = Graph()
g.parse("data/monuments.ttl", format="turtle")

EX = Namespace("http://example.org/monuments#")

# BIND - 1
print("Longitud del nombre de cada monumento")
q1 = """
SELECT ?name ?length WHERE {
  ?m a ex:Monument ; ex:name ?name .
  BIND(STRLEN(?name) AS ?length)
}
"""
for row in g.query(q1, initNs={"ex": EX}):
    print(f" - {row.name} (longitud: {row.length})")

# BIND - 2
print("\nNombre y año formateado como string")
q2 = """
SELECT ?name ?formatted WHERE {
  ?m a ex:Monument ; ex:name ?name ; ex:creationYear ?y .
  BIND(CONCAT(?name, " (", STR(?y), ")") AS ?formatted)
}
"""
for row in g.query(q2, initNs={"ex": EX}):
    print(f" - {row.formatted}")

# IF - 1
print("\n¿El monumento es moderno o antiguo?")
q3 = """
SELECT ?name (IF(?y > "1900-01-01T00:00:00Z"^^xsd:dateTime, "Moderno", "Antiguo") AS ?época) WHERE {
  ?m a ex:Monument ; ex:name ?name ; ex:creationYear ?y .
}
"""
for row in g.query(q3, initNs={"ex": EX, "xsd": XSD}):
    print(f" - {row.name}: {row.época}")

# IF - 2
print("\n¿Tiene tipo definido o no?")
q4 = """
SELECT ?name (IF(BOUND(?type), STR(?type), "Sin tipo") AS ?tipoInfo) WHERE {
  ?m a ex:Monument ; ex:name ?name .
  OPTIONAL { ?m ex:type ?type }
}
"""
for row in g.query(q4, initNs={"ex": EX}):
    print(f" - {row.name}: {row.tipoInfo}")

# UNION - 1
print("\nMonumentos que están en Europa o Asia")
q5 = """
SELECT ?name ?continent WHERE {
  {
    ?m a ex:Monument ; ex:name ?name ; ex:continent "Europe" 
  } UNION {
    ?m a ex:Monument ; ex:name ?name ; ex:continent "Asia"
  }
  ?m ex:continent ?continent .
}
"""
for row in g.query(q5, initNs={"ex": EX}):
    print(f" - {row.name} ({row.continent})")

# UNION - 2
print("\nMonumentos construidos antes del 1600 o en América")
q6 = """
SELECT ?name WHERE {
  {
    ?m a ex:Monument ; ex:name ?name ; ex:creationYear ?y .
    FILTER (?y < "1600-01-01T00:00:00Z"^^xsd:dateTime)
  } UNION {
    ?m a ex:Monument ; ex:name ?name ; ex:continent "Americas" .
  }
}
"""
for row in g.query(q6, initNs={"ex": EX, "xsd": XSD}):
    print(f" - {row.name}")

# STRLEN - 1
print("\nConjunto de monumentos con nombre de más de 25 caracteres, agrupados por paises y mostrando la suma total de sus caracteres")

q = """
SELECT ?monument ?name ?country ?nameLength WHERE {
  ?monument a ex:Monument ;
            ex:name ?name ;
            ex:country ?country .
  BIND(STRLEN(STR(?name)) AS ?nameLength)
  FILTER(?nameLength > 25)
}
ORDER BY DESC(?nameLength)
LIMIT 10
"""

for row in g.query(q, initNs={"ex": EX}):
    print(f" - {row.name} (Country: {row.country}) - Length: {row.nameLength}")

# STRLEN - 2
print("\nMonumentos con nombre largo (más de 30 caracteres), ordenados por longitud descendente:")
q_strlong = """
SELECT ?name (STRLEN(?name) AS ?length) WHERE {
  ?m a ex:Monument ; ex:name ?name .
  FILTER(STRLEN(?name) > 30)
}
ORDER BY DESC(?length)
"""
for row in g.query(q_strlong, initNs={"ex": EX}):
    print(f" - {row.name} ({row.length} caracteres)")

# COALESCE - 1
print("\nEstilo arquitectónico de cada monumento (o 'No architectural style provided'):")
q_coalesce1 = """
SELECT ?name (COALESCE(?architecturalStyle, "No architectural style provided") AS ?styleName) WHERE {
  ?m a ex:Monument ; ex:name ?name .
  OPTIONAL { ?m ex:architecturalStyle ?architecturalStyle }
}
"""
for row in g.query(q_coalesce1, initNs={"ex": EX}):
    print(f" - {row.name}: {row.styleName}")

# COALESCE - 2
print("\nArquitecto de cada monumento (o 'Architect unknown')")
q_coalesce2 = """
SELECT ?name (COALESCE(?hasArchitect, "Architect unknown") AS ?architectName) WHERE {
  ?m a ex:Monument ; ex:name ?name .
  OPTIONAL { ?m ex:hasArchitect ?hasArchitect }
}
"""
for row in g.query(q_coalesce2, initNs={"ex": EX}):
    print(f" - {row.name}: {row.architectName}")

# OPTIONAL - Anidada 1
print("\nMonumentos con arquitecto y año")
q_optional1 = """
SELECT ?name ?hasArchitect (STRBEFORE(STR(?year), "-") AS ?yearOnly) WHERE {
  ?m a ex:Monument ; ex:name ?name .
  OPTIONAL {
    ?m ex:hasArchitect ?hasArchitect .
    OPTIONAL { ?m ex:creationYear ?year }
  }
}
"""
for row in g.query(q_optional1, initNs={"ex": EX}):
    print(f" - {row.name} ({row.yearOnly}): {row.hasArchitect}")

# FILTER - 1
print("\nMonumentos creados después del año 1800 con tipo definido")
q_filter1 = """
SELECT ?name ?year ?type WHERE {
  ?m a ex:Monument ; ex:name ?name ; ex:creationYear ?year .
  OPTIONAL { ?m ex:type ?type }
  FILTER(?year > "1800-01-01T00:00:00"^^xsd:dateTime && bound(?type))
}
"""
for row in g.query(q_filter1, initNs={"ex": EX}):
    print(f" - {row.name}: {row.type}")


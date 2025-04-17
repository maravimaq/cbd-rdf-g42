from rdflib import Graph

g = Graph()
g.parse('data/monuments.ttl', format='ttl')

print("\n ### BIND - Concatenate name and country")
q = '''
SELECT ?monument ?name ?country (CONCAT(?name, ", ", ?country) AS ?label)
WHERE {
  ?monument a ex:Monument ;
            ex:name ?name ;
            ex:country ?country .
}
'''
for row in g.query(q):
    print(row)

print("\n### IF - Style fallback")
q = '''
SELECT ?monument ?name (IF(BOUND(?style), ?style, "No style info") AS ?styleLabel)
WHERE {
  ?monument a ex:Monument ;
            ex:name ?name .
  OPTIONAL { ?monument ex:style ?style . }
}
'''
for row in g.query(q):
    print(row)

print("\n### STRLEN - Name length")
q = '''
SELECT ?monument ?name (STRLEN(?name) AS ?nameLength)
WHERE {
  ?monument a ex:Monument ;
            ex:name ?name .
}
'''
for row in g.query(q):
    print(row)

print("\n### CONTAINS - Name contains 'castle'")
q = '''
SELECT ?monument ?name
WHERE {
  ?monument a ex:Monument ;
            ex:name ?name .
  FILTER(CONTAINS(LCASE(?name), "castle"))
}
'''
for row in g.query(q):
    print(row)

print("\n### UNION - Europe or Gothic")
q = '''
SELECT ?monument ?name ?continent ?style
WHERE {
  {
    ?monument a ex:Monument ;
              ex:name ?name ;
              ex:continent "Europe" .
    OPTIONAL { ?monument ex:style ?style . }
  } UNION {
    ?monument a ex:Monument ;
              ex:name ?name ;
              ex:style "Gothic" .
    OPTIONAL { ?monument ex:continent ?continent . }
  }
}
'''
for row in g.query(q):
    print(row)


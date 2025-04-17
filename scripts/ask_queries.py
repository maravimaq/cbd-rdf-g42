from rdflib import Graph, Namespace

g = Graph()
g.parse("data/monuments.ttl", format="turtle")
EX = Namespace("http://example.org/monuments#")

print("\n ¿Hay monumentos en Australia?")
ask1 = '''
ASK {
  ?m a ex:Monument ;
     ex:country "Australia" .
}
'''
print(bool(g.query(ask1, initNs={"ex": EX})))

print("\n ¿Hay monumentos en Argentina?")
ask2 = '''
ASK {
  ?m a ex:Monument ;
     ex:country "Argentina" .
}
'''
print(bool(g.query(ask2, initNs={"ex": EX})))

print("\n ¿Hay monumentos en Africa?")
ask3 = '''
ASK {
  ?m a ex:Monument ;
     ex:continent "Africa" .
}
'''
print(bool(g.query(ask3, initNs={"ex": EX})))

print("\n ¿Hay algún monumento creado antes del año 0?")
ask4 = '''
ASK {
  ?m a ex:Monument ;
     ex:creationYear ?year .
  FILTER(strstarts(?year, "-") && ?year != "Unknown")
}
'''
print(bool(g.query(ask4, initNs={"ex": EX})))

print("\n ¿Hay algún monumento llamado 'Göbekli Tepe'?")
ask5 = '''
ASK {
  ?m a ex:Monument ;
     ex:name "Göbekli Tepe" .
}
'''
print(bool(g.query(ask5, initNs={"ex": EX})))

print("\n ¿Hay algún monumento en más de un continente?")
ask6 = '''
ASK {
  SELECT ?m (COUNT(DISTINCT ?continent) AS ?count) WHERE {
    ?m a ex:Monument ;
       ex:continent ?continent .
  }
  GROUP BY ?m
  HAVING(?count > 1)
}
'''
print(bool(g.query(ask6, initNs={"ex": EX})))

print("\n ¿Alguno de los monumentos contiene 'Castle' en su nombre?")
ask7 = '''
ASK {
  ?m a ex:Monument ;
     ex:name ?name .
  FILTER(CONTAINS(LCASE(?name), "castle"))
}
'''
print(bool(g.query(ask7, initNs={"ex": EX})))

print("\n ¿Hay monumentos en in Peru?")
ask8 = '''
ASK {
  ?m a ex:Monument ;
     ex:country "Peru" .
}
'''
print(bool(g.query(ask8, initNs={"ex": EX})))

print("\n ¿Hay monumentos en Laos?")
ask9 = '''
ASK {
  ?m a ex:Monument ;
     ex:country "Laos" .
}
'''
print(bool(g.query(ask9, initNs={"ex": EX})))

print("\n ¿Hay monumentos de tipo 'cave painting'?")
ask10 = '''
ASK {
  ?m a ex:Monument ;
     ex:type ?type .
  FILTER(CONTAINS(LCASE(?type), "cave painting"))
}
'''
print(bool(g.query(ask10, initNs={"ex": EX})))

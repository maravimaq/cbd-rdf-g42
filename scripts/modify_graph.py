from rdflib import Graph, Namespace, URIRef, Literal, ConjunctiveGraph
from datetime import datetime
from rdflib.namespace import RDF, XSD

g = Graph()
g.parse("data/monuments.ttl", format="ttl")

EX = Namespace("http://example.org/monuments#")

constructed = Graph()

# Monumentos en Asia creados despues del año 1000
construct_query = """
PREFIX ex: <http://example.org/monuments#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

CONSTRUCT {
  ?monument a ex:Monument ;
            ex:continent "Asia" ;
            ex:creationYear ?year ;
            ex:name ?name .
}
WHERE {
  ?monument a ex:Monument ;
             ex:continent "Asia" ;
             ex:creationYear ?year ;
             ex:name ?name .
  FILTER (xsd:dateTime(?year) > "1000-01-01T00:00:00Z"^^xsd:dateTime)
}
"""
constructed += g.query(construct_query)
constructed.serialize(destination="data/modified_graphs/original_graph.ttl", format="ttl")

# Eliminar fecha de creación de Zeyrek Mosque
zeyrek_uri = URIRef("http://www.wikidata.org/entity/Q197094")
constructed.remove((zeyrek_uri, EX.creationYear, None))

# Modificar nombre de Himeji Castle
himeji_uri = URIRef("http://www.wikidata.org/entity/Q188754")
constructed.remove((himeji_uri, EX.name, Literal("Himeji Castle")))
constructed.add((himeji_uri, EX.name, Literal("Himeji Fortress")))

# Añadir tipo al monumento Gobustan
gobustan_uri = URIRef("http://www.wikidata.org/entity/Q318181")
constructed.add((gobustan_uri, EX.type, Literal("Rock Art Site")))

# Añadir tipo al monumento Gobustan
gobustan_uri = URIRef("http://www.wikidata.org/entity/Q318181")
constructed.add((gobustan_uri, EX.type, Literal("Rock Art Site")))

# Cambiar el nombre de Selimiye Mosque
for subj, pred, obj in constructed.triples((None, EX.name, Literal("Selimiye Mosque"))):
    constructed.set((subj, EX.name, Literal("Selimiye Mosque (Edirne)")))

# Cambiar el año de creación del monumento Kaziranga National Park
constructed.update("""
PREFIX ex: <http://example.org/monuments#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

DELETE {
  ?m ex:creationYear "1905-01-01T00:00:00+00:00"^^xsd:dateTime .
}
INSERT {
  ?m ex:creationYear "1906-01-01T00:00:00+00:00"^^xsd:dateTime .
}
WHERE {
  ?m a ex:Monument ;
     ex:name "Kaziranga National Park" ;
     ex:creationYear "1905-01-01T00:00:00+00:00"^^xsd:dateTime .
}
""")

#Cambiar el nombre del monumento Sinharaja Forest Reserve
for s, p, o in constructed.triples((None, EX.name, Literal("Sinharaja Forest Reserve"))):
    constructed.remove((s, EX.name, o))
    constructed.add((s, EX.name, Literal("Sinharaja Grand Forest Reserve")))

constructed.serialize(destination="data/modified_graphs/simple_modifications_graph.ttl", format="ttl")

# Modificar nombres con `.value()`
for subj in constructed.subjects(predicate=EX.continent, object=Literal("Asia")):
    year_literal = constructed.value(subject=subj, predicate=EX.creationYear)
    if year_literal:
        try:
            year = datetime.fromisoformat(str(year_literal))
            if year.year > 1500:
                print(f"Modificando nombre de {subj}")
                constructed.set((subj, EX.name, Literal("POST1500_" + str(constructed.value(subj, EX.name)))))
        except Exception as e:
            print(f"Error procesando fecha: {year_literal} - {e}")

constructed.serialize("data/modified_graphs/value_modifications_graph.ttl", format="ttl")

# Añadir 3 monumentos nuevos
new_monuments = {
    "QPetra": {
        "name": "Petra",
        "creationYear": "0100-01-01T00:00:00+00:00",
        "continent": "Asia"
    },
    "QBamiyan": {
        "name": "Bamiyan Valley",
        "creationYear": "0500-01-01T00:00:00+00:00",
        "continent": "Asia"
    },
    "QBorobudur": {
        "name": "Borobudur",
        "creationYear": "0800-01-01T00:00:00+00:00",
        "continent": "Asia"
    }
}

for qid, data in new_monuments.items():
    uri = URIRef(f"http://example.org/monuments#{qid}")
    constructed.add((uri, RDF.type, EX.Monument))
    constructed.add((uri, EX.name, Literal(data["name"])))
    constructed.add((uri, EX.creationYear, Literal(data["creationYear"], datatype=XSD.dateTime)))
    constructed.add((uri, EX.continent, Literal(data["continent"])))

# Añadir tipo a todos los monumentos
for subj in constructed.subjects(RDF.type, EX.Monument):
    constructed.add((subj, EX.type, Literal("Cultural Heritage Site")))

# Modificar la fecha de creación de los 3 monumentos añadidos nuevos
for qid in new_monuments:
    uri = URIRef(f"http://example.org/monuments#{qid}")
    constructed.set((uri, EX.creationYear, Literal("1067-01-01T00:00:00+00:00", datatype=XSD.dateTime)))

# 4. Eliminar el continente de todos los monumentos
constructed.remove((None, EX.continent, None))

constructed.serialize("data/modified_graphs/complex_modifications_graph.ttl", format="ttl")

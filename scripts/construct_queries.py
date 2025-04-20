from rdflib import Graph, Literal, Namespace
import os

g = Graph()
g.parse("data/monuments.ttl", format="turtle")
EX = Namespace("http://example.org/monuments#")

output_dir = "data/construct_graphs"
os.makedirs(output_dir, exist_ok=True)

def save_graph(graph, name):
    monuments = {s for s in graph.subjects() if (s, None, None) in graph}
    path = os.path.join(output_dir, f"{name}.ttl")
    graph.serialize(destination=path, format="turtle")
    print(f"{name} ({len(monuments)} monumentos) -> Guardado en: {path}")

def run_construct(query, name):
    g2 = g.query(query, initNs={"ex": EX})
    save_graph(g2.graph, name)

print('\nGrafo con todos los monumentos y su país')
run_construct("""
CONSTRUCT {
  ?m ex:country ?country .
}
WHERE {
  ?m a ex:Monument ;
     ex:country ?country .
}
""", "monuments_with_country")

print('\nGrafo con monumentos en Europa')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:continent "Europe" ;
     ?p ?o .
}
""", "monuments_in_europe")

print('\nGrafo con monumentos en Asia')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:continent "Asia" ;
     ?p ?o .
}
""", "monuments_in_asia")

print('\nGrafo con monumentos en América del Norte')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:continent "North America" ;
     ?p ?o .
}
""", "monuments_in_north_america")

print('\nGrafo con monumentos en América del Sur')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:continent "South America" ;
     ?p ?o .
}
""", "monuments_in_south_america")

print('\nGrafo con monumentos en África')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:continent "Africa" ;
     ?p ?o .
}
""", "monuments_in_africa")

print('\nGrafo con monumentos en Oceanía')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:continent "Oceania" ;
     ?p ?o .
}
""", "monuments_in_oceania")

print('\nGrafo con monumentos y su estilo arquitectónico')
run_construct("""
CONSTRUCT {
  ?m ex:architecturalStyle ?style .
}
WHERE {
  ?m a ex:Monument ;
     ex:architecturalStyle ?style .
}
""", "monuments_with_style")

print('\nMonumentos con arquitectos conocidos')
run_construct("""
CONSTRUCT {
  ?m ex:hasArchitect ?a .
}
WHERE {
  ?m a ex:Monument ;
     ex:hasArchitect ?a .
}
""", "monuments_with_architect")

print('\nMonumentos en países específicos (Italia, Francia y España)')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:country ?country ;
     ?p ?o .
  FILTER (?country IN ("Italy", "France", "Spain"))
}
""", "monuments_in_specific_countries")

print('\nMonumentos con tipo definido')
run_construct("""
CONSTRUCT {
  ?m ex:type ?type .
}
WHERE {
  ?m a ex:Monument ;
     ex:type ?type .
}
""", "monuments_with_type")

print('\nMonumentos con año de creación')
run_construct("""
CONSTRUCT {
  ?m ex:creationYear ?year .
}
WHERE {
  ?m a ex:Monument ;
     ex:creationYear ?year .
}
""", "monuments_with_year")

print('\nGrafo reducido a propiedades name y country')
run_construct("""
CONSTRUCT {
  ?m ex:name ?name ;
     ex:country ?country .
}
WHERE {
  ?m a ex:Monument ;
     ex:name ?name ;
     ex:country ?country .
}
""", "monuments_name_and_country")

print('\nMonumentos en Europa con estilo arquitectónico gótico')
run_construct("""
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:continent "Europe" ;
     ex:architecturalStyle "Gothic architecture" ;
     ?p ?o .
}
""", "gothic_monuments_in_europe")

print('\nSubgrafo de monumentos creados antes del año 1500')
run_construct("""
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
CONSTRUCT {
  ?m ?p ?o .
}
WHERE {
  ?m a ex:Monument ;
     ex:creationYear ?year ;
     ?p ?o .
  FILTER(xsd:integer(SUBSTR(STR(?year), 1, 4)) < 1500)
}
""", "monuments_before_1500")


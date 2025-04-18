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

print('\nGrafo con todos los monumentos y su país')
g2 = Graph()
for s, o in g.subject_objects(EX.country):
    g2.add((s, EX.country, o))
save_graph(g2, "monuments_with_country")

print('\nGrafo con monumentos en Europa')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("Europe")):
    g2 += g.triples((s, None, None))
save_graph(g2, "monuments_in_europe")

print('\nGrafo con monumentos en Asia')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("Asia")):
    g2 += g.triples((s, None, None))
save_graph(g2, "monuments_in_asia")

print('\nGrafo con monumentos en América del Norte')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("North America")):
    g2 += g.triples((s, None, None))
save_graph(g2, "monuments_in_north_america")

print('\nGrafo con monumentos en América del Sur')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("South America")):
    g2 += g.triples((s, None, None))
save_graph(g2, "monuments_in_south_america")

print('\nGrafo con monumentos en África')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("Africa")):
    g2 += g.triples((s, None, None))
save_graph(g2, "monuments_in_africa")

print('\nGrafo con monumentos en Oceanía')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("Oceania")):
    g2 += g.triples((s, None, None))
save_graph(g2, "monuments_in_oceania")

print('\nGrafo con monumentos y su estilo arquitectónico')
g2 = Graph()
for s, o in g.subject_objects(EX.architecturalStyle):
    g2.add((s, EX.architecturalStyle, o))
save_graph(g2, "monuments_with_style")

print('\nMonumentos con arquitectos conocidos')
g2 = Graph()
for s, o in g.subject_objects(EX.hasArchitect):
    g2.add((s, EX.hasArchitect, o))
save_graph(g2, "monuments_with_architect")

print('\nMonumentos en países específicos(Italia, Francia y España)')
target_countries = {"Italy", "France", "Spain"}
g2 = Graph()
for s, o in g.subject_objects(EX.country):
    if str(o) in target_countries:
        g2 += g.triples((s, None, None))
save_graph(g2, "monuments_in_specific_countries")

print('\nMonumentos con tipo definido')
g2 = Graph()
for s, o in g.subject_objects(EX.type):
    g2.add((s, EX.type, o))
save_graph(g2, "monuments_with_type")

print('\nMonumentos con año de creación')
g2 = Graph()
for s, o in g.subject_objects(EX.creationYear):
    g2.add((s, EX.creationYear, o))
save_graph(g2, "monuments_with_year")

print('\nGrafo reducido a propiedades name y country')
g2 = Graph()
for s in g.subjects(predicate=EX.name):
    g2.add((s, EX.name, g.value(s, EX.name)))
    g2.add((s, EX.country, g.value(s, EX.country)))
save_graph(g2, "monuments_name_and_country")

print('\nMonumentos en Europa con estilo arquitectónico gótico')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("Europe")):
    if g.value(s, EX.architecturalStyle) == Literal("Gothic architecture"):
        g2 += g.triples((s, None, None))
save_graph(g2, "gothic_monuments_in_europe")

print('\nSubgrafo de monumentos creados antes del año 1500')
g2 = Graph()
for s, y in g.subject_objects(EX.creationYear):
    if str(y).isdigit() and int(str(y)) < 1500:
        g2 += g.triples((s, None, None))
save_graph(g2, "monuments_before_1500")

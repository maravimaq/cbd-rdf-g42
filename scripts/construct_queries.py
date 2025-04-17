from rdflib import Graph, Literal, Namespace

g = Graph()
g.parse("data/monuments.ttl", format="turtle")
EX = Namespace("http://example.org/monuments#")

print('Grafo con todos los monumentos y su país')
g2 = Graph()
for s, o in g.subject_objects(EX.country):
    g2.add((s, EX.country, o))
print(len(g2))

print('Grafo con monumentos en Europa')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("Europe")):
    g2 += g.triples((s, None, None))
print(len(g2))

print('Grafo con monumentos y su estilo arquitectónico')
g2 = Graph()
for s, o in g.subject_objects(EX.architecturalStyle):
    g2.add((s, EX.architecturalStyle, o))
print(len(g2))

print('Monumentos con arquitectos conocidos')
g2 = Graph()
for s, o in g.subject_objects(EX.hasArchitect):
    g2.add((s, EX.hasArchitect, o))
print(len(g2))

print('Monumentos en países específicos')
target_countries = {"Italy", "France", "Spain"}
g2 = Graph()
for s, o in g.subject_objects(EX.country):
    if str(o) in target_countries:
        g2 += g.triples((s, None, None))
print(len(g2))

print('Monumentos con tipo definido')
g2 = Graph()
for s, o in g.subject_objects(EX.type):
    g2.add((s, EX.type, o))
print(len(g2))

print('Monumentos con año de creación')
g2 = Graph()
for s, o in g.subject_objects(EX.creationYear):
    g2.add((s, EX.creationYear, o))
print(len(g2))

print('Grafo reducido a propiedades name y country')
g2 = Graph()
for s in g.subjects(predicate=EX.name):
    g2.add((s, EX.name, g.value(s, EX.name)))
    g2.add((s, EX.country, g.value(s, EX.country)))
print(len(g2))

print('Monumentos en Europa con estilo arquitectónico gótico')
g2 = Graph()
for s in g.subjects(EX.continent, Literal("Europe")):
    if g.value(s, EX.architecturalStyle) == Literal("Gothic architecture"):
        g2 += g.triples((s, None, None))
print(len(g2))

print('Subgrafo de monumentos creados antes del año 1500')
g2 = Graph()
for s, y in g.subject_objects(EX.creationYear):
    if str(y).isdigit() and int(str(y)) < 1500:
        g2 += g.triples((s, None, None))
print(len(g2))
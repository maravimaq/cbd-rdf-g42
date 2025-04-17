from rdflib import Graph, Literal, Namespace
import re

g = Graph()
g.parse("data/monuments.ttl", format="turtle")
EX = Namespace("http://example.org/monuments#")

print('\nMonumentos creados antes del año 1000 y con estilo románico')
for s, year in g.subject_objects(EX.creationYear):
    if year:
        try:
            y = int(str(year)[:4])
            style = g.value(s, EX.architecturalStyle)
            if y < 1000 and style and "roman" in style.lower():
                print(f"\t {g.value(s, EX.name)} creado en {y} con estilo {style}")
        except ValueError:
            continue

print('\n Monumentos sin tipo definido pero con arquitecto')
for s in g.subjects(predicate=EX.hasArchitect):
    if not g.value(s, EX.type):
        print(f"\t {g.value(s, EX.name)} tiene arquitecto pero no tipo")

print('\n Número de monumentos por continente')
from collections import Counter
cont = Counter(g.objects(predicate=EX.continent))
for k, v in cont.items():
    print(f"\t {k}: {v}")

print('\n Monumentos que comparten arquitecto')
from collections import defaultdict
arquitectos = defaultdict(list)
for s, a in g.subject_objects(EX.hasArchitect):
    arquitectos[a].append(s)
for a, lst in arquitectos.items():
    if len(lst) > 1:
        print(f"\t Arquitecto {a} en múltiples monumentos:")
        for s in lst:
            print(f"\t  - {g.value(s, EX.name)}")

print('\n Monumentos cuyo país pertenece a América y tienen más de 20 caracteres en el nombre')
for s, country in g.subject_objects(EX.country):
    cont = g.value(s, EX.continent)
    name = g.value(s, EX.name)
    if cont and "America" in str(cont) and name and len(str(name)) > 20:
        print(f"\t {name} - {country} ({cont})")

print('\n Monumentos cuya creación fue en el siglo XIX (1800-1899)')
for s, y in g.subject_objects(EX.creationYear):
    match = re.match(r'^(\d{4})', str(y))
    if match:
        year = int(match.group(1))
        if 1800 <= year <= 1899:
            print(f"\t {g.value(s, EX.name)} creado en el siglo XIX")

print('\n Monumentos con nombre que empieza por "S"')
for s, n in g.subject_objects(EX.name):
    if str(n).startswith("S"):
        print(f"\t Nombre con S: {n}")

print('\n Monumentos con todos los campos: nombre, país, año, estilo y arquitecto')
for s in g.subjects():
    if all(g.value(s, p) for p in [EX.name, EX.country, EX.creationYear, EX.architecturalStyle, EX.hasArchitect]):
        print(f"\t Completo: {g.value(s, EX.name)}")

print('\n Agrupar monumentos por estilo arquitectónico')
from collections import defaultdict
estilos = defaultdict(list)
for s, e in g.subject_objects(EX.architecturalStyle):
    estilos[e].append(g.value(s, EX.name))
for estilo, nombres in estilos.items():
    print(f"\t Estilo: {estilo}")
    for n in nombres:
        print(f"\t  - {n}")
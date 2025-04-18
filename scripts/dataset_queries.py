from rdflib import Dataset, Graph, Namespace
import os

dataset = Dataset()
data_dir = "data/construct_graphs"
EX = Namespace("http://example.org/monuments#")

default_graph = dataset.default_context

for filename in os.listdir(data_dir):
    if filename.endswith(".ttl"):
        graph_uri = f"http://example.org/context/{filename}"
        g_named = dataset.graph(graph_uri)
        path = os.path.join(data_dir, filename)
        g_named.parse(path, format="turtle")

        for triple in g_named:
            default_graph.add(triple)

print("Grafos nombrados cargados:")
for ctx in dataset.contexts():
    print("-", ctx.identifier)

graph_individual = Graph()
graph_individual.parse(os.path.join(data_dir, "monuments_in_europe.ttl"), format="turtle")

query_plain = """
PREFIX ex: <http://example.org/monuments#>
SELECT ?monument ?country ?style
WHERE {
  ?monument ex:country ?country .
  OPTIONAL { ?monument ex:architecturalStyle ?style }
}
LIMIT 10
"""


query_with_graph = """
PREFIX ex: <http://example.org/monuments#>
SELECT ?monument ?country ?style
WHERE {
  GRAPH <http://example.org/context/monuments_in_europe.ttl> {
    ?monument ex:country ?country .
    OPTIONAL { ?monument ex:architecturalStyle ?style }
  }
}
LIMIT 10
"""

def print_pretty(title, results, cols=["Monument", "Country", "Style"]):
    print(f"\n {title}")
    results = list(results)
    if not results:
        print(" No se encontraron resultados.")
        return

    col_widths = [max(len(str(row[i])) for row in results) if results else len(col) for i, col in enumerate(cols)]
    col_widths = [max(len(c), w) for c, w in zip(cols, col_widths)]

    
    header = " | ".join(col.ljust(w) for col, w in zip(cols, col_widths))
    print(header)
    print("-" * len(header))

    
    for row in results:
        formatted = " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
        print(formatted)


print_pretty("1. Resultados desde grafo individual (Graph)", graph_individual.query(query_plain))
print_pretty("2. Resultados desde el Dataset completo (todos los grafos)", dataset.query(query_plain))
print_pretty("3. Resultados desde Dataset con cláusula GRAPH", dataset.query(query_with_graph))
g_named = dataset.graph("http://example.org/context/monuments_in_europe.ttl")
print_pretty("4. Resultados desde el grafo nombrado extraído del Dataset", g_named.query(query_plain))

query_ask_plain = """
PREFIX ex: <http://example.org/monuments#>
ASK {
  ?m ex:country "France" .
}
"""

query_ask_graph = """
PREFIX ex: <http://example.org/monuments#>
ASK {
  GRAPH <http://example.org/context/monuments_in_europe.ttl> {
    ?m ex:country "France" .
  }
}
"""

print("\nASK desde grafo individual:", graph_individual.query(query_ask_plain).askAnswer)
print("ASK desde dataset completo:", dataset.query(query_ask_plain).askAnswer)
print("ASK desde dataset con GRAPH:", dataset.query(query_ask_graph).askAnswer)
print("ASK desde grafo nombrado:", g_named.query(query_ask_plain).askAnswer)

query_describe_plain = """
PREFIX ex: <http://example.org/monuments#>
DESCRIBE <http://www.wikidata.org/entity/Q201428>
"""

query_describe_graph = """
PREFIX ex: <http://example.org/monuments#>
DESCRIBE <http://www.wikidata.org/entity/Q201428>
"""

def print_triples(title, result_graph):
    print(f"\n {title}")
    for s, p, o in result_graph:
        print(f"{s} -- {p} --> {o}")

print_triples("1. DESCRIBE desde grafo individual", graph_individual.query(query_describe_plain))
print_triples("2. DESCRIBE desde dataset completo", dataset.query(query_describe_plain))
print_triples("3. DESCRIBE desde dataset con GRAPH", dataset.query(query_describe_graph))
print_triples("4. DESCRIBE desde grafo nombrado", g_named.query(query_describe_plain))


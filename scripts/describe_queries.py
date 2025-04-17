from rdflib import Graph, Namespace
from collections import defaultdict

g = Graph()
g.parse("data/monuments.ttl", format="turtle")

EX = Namespace("http://example.org/monuments#")

def run_describe_query(title, query):
    print(f"\n{title}")
    results = g.query(query)
    
    grouped = defaultdict(list)
    for s, p, o in results.graph:
        grouped[s].append((p, o))
    
    for i, (sujeto, props) in enumerate(grouped.items(), 1):
        print(f"\nMonumento {i}: {sujeto}")
        for p, o in props:
            print(f"  {p} => {o}")

queries = [
    ("Monumentos en Peru", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:country "Peru" .
        }
    '''),
    ("Monumentos de estilo arquitectónico gótico", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:architecturalStyle "Gothic architecture" .
        }
    '''),
    ("Monumentos diseñados por Antonine Wall", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:hasArchitect "Antonine Wall" .
        }
    '''),
    ("Monumentos del siglo 20", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:creationYear ?year .
            FILTER(STR(?year) >= "1900" && STR(?year) <= "2000")
        }
    '''),
    ("Monumentos de Asia", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:continent "Asia" .
        }
    '''),
    ("Monumentos de tipo escultura", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:type "monumental sculpture" .
        }
    '''),
    ("Monumentos en Francia", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:country "France" .
        }
    '''),
    ("Monumentos de América del Sur", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:continent "South America" .
        }
    '''),
    ("Monumentos en África", '''
        PREFIX ex: <http://example.org/monuments#>
        DESCRIBE ?m WHERE {
            ?m a ex:Monument ;
               ex:continent "Africa" .
        }
    ''')
]

for title, query in queries:
    run_describe_query(title, query)

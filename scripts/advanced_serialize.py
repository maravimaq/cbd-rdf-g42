import os
from rdflib import Graph

INPUT_DIR = "data/construct_graphs"
OUTPUT_ROOT = "data/construct_graphs/serialized_graphs"
FORMATS = {
    "xml": ".rdf",
    "n3": ".n3",
    "nt": ".nt",
    "json-ld": ".jsonld"
}

os.makedirs(OUTPUT_ROOT, exist_ok=True)

for fmt, ext in FORMATS.items():
    format_dir = os.path.join(OUTPUT_ROOT, fmt)
    os.makedirs(format_dir, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".ttl"):
        path = os.path.join(INPUT_DIR, filename)
        g = Graph()
        g.parse(path, format="turtle")
        
        base_name = os.path.splitext(filename)[0]

        for fmt, ext in FORMATS.items():
            output_path = os.path.join(OUTPUT_ROOT, fmt, base_name + ext)
            g.serialize(destination=output_path, format=fmt, encoding="utf-8")
            print(f"Serializado en {fmt}: {output_path}")
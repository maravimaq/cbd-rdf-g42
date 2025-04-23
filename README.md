
# Proyecto sobre RDFLib

## Estructura del Proyecto

```
├── data/
│   ├── construct_graphs/
│   │   ├── [subgrafos .ttl generados]
│   │   └── serialized_graphs/
│   │       ├── json-ld/
│   │       ├── n3/
│   │       ├── nt/
│   │       └── xml/
│   ├── modified_graphs/
│   │   ├── original_graph.ttl
│   │   ├── simple_modifications_graph.ttl
│   │   ├── complex_modifications_graph.ttl
│   │   ├── value_modifications_graph.ttl
│   └── monuments.ttl
├── scripts/
│   ├── download_data.py
│   ├── construct_queries.py
│   ├── ask_queries.py
│   ├── select_queries.py
│   ├── describe_queries.py
│   ├── direct_queries.py
│   ├── advanced_queries.py
│   ├── advanced_serialize.py
│   ├── modify_graph.py
│   ├── dataset_queries.py
├── .venv/
├── README.md
```

---

## 1. Instalación

### Requisitos
- Python 3.8.1 o superior
- `pip` para instalación de paquetes

### Instalación de dependencias

```bash
pip install rdflib SPARQLWrapper
```

---

## 2. Ejecución de Funcionalidades

Cada script realiza una funcionalidad específica y se encuentra en la carpeta `scripts/`.

| Script | Funcionalidad |
|--------|----------------|
| `download_data.py` | Descarga datos RDF desde Wikidata y genera `monuments.ttl` |
| `construct_queries.py` | Genera subgrafos RDF (.ttl) por continente, tipo, estilo... |
| `advanced_serialize.py` | Serializa todos los subgrafos `.ttl` a `.rdf`, `.n3`, `.nt`, `.jsonld` |
| `select_queries.py` | Ejecuta consultas SELECT SPARQL |
| `ask_queries.py` | Ejecuta consultas ASK SPARQL |
| `describe_queries.py` | Ejecuta consultas DESCRIBE SPARQL |
| `advanced_queries.py` | Ejecuta consultas con BIND, IF, UNION, etc. |
| `direct_queries.py` | Consultas directas RDFLib sin SPARQL |
| `dataset_queries.py` | Consultas sobre múltiples grafos RDF nombrados |
| `modify_graph.py` | Aplica modificaciones a un grafo RDF (elimina, agrega, cambia triples) |

### Ejemplo de ejecución:

```bash
python scripts/construct_queries.py
python scripts/advanced_serialize.py
```

---

## 3. Manual de Usuario

Este sistema permite trabajar con un grafo RDF sobre Monumentos Patrimonio de la Humanidad.  
Se puede:

- Descargar datos de forma automática desde Wikidata.
- Realizar consultas SPARQL:`SELECT`, `ASK`, `DESCRIBE`, `CONSTRUCT`.
- Generar subgrafos temáticos.
- Serializar los subgrafos en distintos formatos.
- Modificar el grafo (añadir, eliminar, editar triples).
- Ejecutar consultas complejas con operadores avanzados.
- Buscar información directamente con RDFLib.

### Ejemplos

- Ver monumentos en Europa → `monuments_in_europe.ttl`
- Ver monumentos góticos → `gothic_monuments_in_europe.ttl`
- Consultar si existe el monumento "Göbekli Tepe" → `ask_queries.py`
- Modificar nombre de "Himeji Castle" → `modify_graph.py`



---



Archivo generado por ChatGPT:  https://chatgpt.com/share/6807f415-1178-800a-8418-081190724e91

----
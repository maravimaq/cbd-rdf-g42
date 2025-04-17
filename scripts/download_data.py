from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD
import datetime

print("Downloading data from Wikidata...")

# Setup SPARQL
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery("""
SELECT ?monument ?monumentLabel ?countryLabel ?continentLabel ?year ?typeLabel ?architectLabel ?styleLabel WHERE {
  ?monument wdt:P1435 wd:Q9259.
  ?monument wdt:P17 ?country.
  OPTIONAL { ?country wdt:P30 ?continent. }
  OPTIONAL { ?monument wdt:P571 ?year. }
  OPTIONAL { ?monument wdt:P136 ?type. }
  OPTIONAL { ?monument wdt:P84 ?architect. }
  OPTIONAL { ?monument wdt:P149 ?style. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 200
""")

results = sparql.query().convert()

# Namespaces
EX = Namespace("http://example.org/monuments#")
g = Graph()
g.bind("ex", EX)

for result in results["results"]["bindings"]:
    uri = URIRef(result["monument"]["value"])
    g.add((uri, RDF.type, EX.Monument))

    name = result.get("monumentLabel", {}).get("value", None)
    if name:
        g.add((uri, EX.name, Literal(name)))

    country = result.get("countryLabel", {}).get("value", None)
    if country:
        g.add((uri, EX.country, Literal(country)))

    continent = result.get("continentLabel", {}).get("value", None)
    if continent:
        g.add((uri, EX.continent, Literal(continent)))

    year = result.get("year", {}).get("value", None)
    if year and "T" in year and not year.startswith("-"):
        try:
            g.add((uri, EX.creationYear, Literal(year, datatype=XSD.dateTime)))
        except:
            g.add((uri, EX.creationYear, Literal(year)))
    elif year:
        g.add((uri, EX.creationYear, Literal(year)))


    monument_type = result.get("typeLabel", {}).get("value", None)
    if monument_type:
        g.add((uri, EX.type, Literal(monument_type)))

    architect = result.get("architectLabel", {}).get("value", None)
    if architect:
        g.add((uri, EX.hasArchitect, Literal(architect)))

    style = result.get("styleLabel", {}).get("value", None)
    if style:
        g.add((uri, EX.architecturalStyle, Literal(style)))

# Save to TTL
g.serialize("/data/monuments.ttl", format="turtle")
print("Data saved to monuments.ttl")

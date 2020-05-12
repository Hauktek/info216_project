from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON
import urllib

def enrich_data(ent):
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    sparqlDB.setQuery("""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT ?label ?description
    WHERE { dbr:"""

    + ent + 

    """ rdfs:label ?label.

    FILTER (langMatches(lang(?label),"en"))

    }
    """)

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()


    for result in results["results"]["bindings"]:
        print(result["label"]["value"])
        print(result["description"]["value"])



enrich_data("90_Days_%28%66ilm%29")

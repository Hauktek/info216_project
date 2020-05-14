from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON
import urllib

def enrich_data():
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    sparqlDB.setQuery("""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?x
        WHERE { dbr:Barack_Obama a ?x.
        
        }""")

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()

    for result in results["results"]["bindings"]:
        if 'http://dbpedia.org/ontology/' in result['x']['value']:
            i = result['x']['value'].split('http://dbpedia.org/ontology/')

            print(i[1])



             





       



enrich_data()
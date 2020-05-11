from SPARQLWrapper import SPARQLWrapper, JSON
import urllib

def enrich_data(entity):
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    prefixDBP = "PREFIX dbp: <http://dbpedia.org/resource/> "
    prefixDBO = "PREFIX dbo: <http://dbpedia.org/ontology/> "
    prefixRDFS = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "

    ent = urllib.parse.quote(entity)

    queryString = prefixDBP + prefixRDFS + ' SELECT ?label WHERE { dbp:' + ent + ' rdfs:label ?label. FILTER (langMatches(lang(?label),"en")) }'

    sparqlDB.setQuery(queryString)

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()

    for result in results["results"]["bindings"]:
        print(result["label"]["value"])

enrich_data("Jersey_Express_S%2EC%2E")


# sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# sparql.setQuery("""
#     PREFIX dbr: <http://dbpedia.org/resource/>
#     PREFIX dbo: <http://dbpedia.org/ontology/>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?comment
#     WHERE {
#     dbr:90_Days_(film) rdfs:label ?comment.
#     FILTER (langMatches(lang(?comment),"en"))
#     }
# """)

# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()

# for result in results["results"]["bindings"]:
#     print(result["comment"]["value"])
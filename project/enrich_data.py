from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON
import urllib

def enrich_data(entity):
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    prefixDBP = "PREFIX dbp: <http://dbpedia.org/resource/> "
    prefixDBO = "PREFIX dbo: <http://dbpedia.org/ontology/> "
    prefixRDFS = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "

    ent = urllib.parse.quote(entity)
    ent = ent.replace(".","%2E")

    queryString = prefixDBP + prefixRDFS + ' SELECT ?label WHERE { dbp:' + ent + ' rdfs:label ?label. FILTER (langMatches(lang(?label),"en")) }'

    sparqlDB.setQuery(queryString)

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()

    return results












# sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

# sparqlDB.setQuery("""
#     PREFIX dbp: <http://dbpedia.org/resource/>
#     PREFIX dbo: <http://dbpedia.org/ontology/>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?comment
#     WHERE {
#     dbp:Barack_Obama rdfs:label ?comment.
#     FILTER (langMatches(lang(?comment),"en"))
#     }
# """)






# sparqlDB.setReturnFormat(JSON)
# results = sparqlDB.query().convert()

# for result in results["results"]["bindings"]:
#     print(result["comment"]["value"])



# namespace = "test"
# sparql = SPARQLWrapper("http://10.0.0.6:9999/blazegraph/namespace/"+ namespace + "/sparql")

# sparql.setMethod(POST)

# sparql.setQuery("""
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX dbp: <http://dbpedia.org/resource/>
#     INSERT DATA{
#     dbp:Barack_Obama rdfs:label "Barack Obama".
#     }
# """)

# results = sparql.query()
# print(results.response.read())
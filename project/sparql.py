from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON

#java -server -Xmx4g -jar blazegraph.jar

namespace = "test"
sparql = SPARQLWrapper("http://10.0.0.6:9999/blazegraph/namespace/"+ namespace + "/sparql")

prefixSchema = "PREFIX schema: <http://schema.org/> "
prefixExample = "PREFIX ex: <http://example.org/> "
prefixRdf = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "




def makeQuery(searchString):
    queryString = prefixSchema + ' SELECT DISTINCT ?s WHERE { ?s <https://schema.org/author> ' + '"' + searchString + '". }'
    
    return queryString


#print(makeQuery("chappachula"))

sparql.setQuery(makeQuery("chappachula"))
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"])

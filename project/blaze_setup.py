from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON

#java -server -Xmx4g -jar blazegraph.jar

namespace = "kb"
sparql = SPARQLWrapper("http://10.0.0.6:9999/blazegraph/namespace/"+ namespace + "/sparql")

sparql.setMethod(POST)

sparql.setQuery("""
    load <file:////Users/andrius/Documents/Github/info216_project/triples.ttl>
""")

results = sparql.query()
print(results.response.read())



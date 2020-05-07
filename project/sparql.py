from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON

class spa:
    #java -server -Xmx4g -jar blazegraph.jar

    namespace = "test"
    sparql = SPARQLWrapper("http://10.0.0.6:9999/blazegraph/namespace/"+ namespace + "/sparql")


    def makeQuery(searchString):
        print(searchString)



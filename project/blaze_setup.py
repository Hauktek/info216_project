from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON

# Download blazegraph.jar file from https://blazegraph.com/ and move it to project folder.
# Use the terminal on the computer (not the one in IDE), navigate to the project folder where blazegraph.jar is. 
# Use the command "java -server -Xmx4g -jar blazegraph.jar" to run blazegraph. 
# There should appear a url to blazegraph in the terminal, change the one that is in SPARQLWrapper if it is different, but include the /blazegraph/namespace/ at the end. 
# Find the filepath to the project folder where the "triples.ttl" file will be and use it in the load querie with /triples.ttl ending.
# It is important to use full filepath.
# The filepath may differ from windows and mac. The example below is usen on mac. 
# If for some reason this would not work, comment out the functioncall from rdf_setup.py, run it to get the file with triples and manually upload to blazegraph.


# This function uploads a turtle file with triples to blazegraph. 
def blaze_uploader(): 
    namespace = "test"
    sparql = SPARQLWrapper("http://10.0.0.6:9999/blazegraph/namespace/"+ namespace + "/sparql")

    sparql.setMethod(POST)

    sparql.setQuery("""
        load <file:////Users/andrius/Documents/Github/info216_project/triples.ttl>
    """)

    results = sparql.query()
    print(results.response.read())





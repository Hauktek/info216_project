from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON
import urllib

# A function for finding additional data for the entities. Types, label, comment and description. 
# Connects to dbpedia sparql endpoint. 
def find_data(entity):
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    ent = urllib.parse.quote(entity)
    ent = ent.replace(".","%2E")

    sparqlDB.setQuery("""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?type ?label ?comment ?description
        WHERE { 
            dbr:""" + ent + """ a ?type.
        OPTIONAL {dbr:""" + ent + """ rdfs:label ?label. FILTER (langMatches(lang(?label),"en"))}
        OPTIONAL {dbr:""" + ent + """ rdfs:comment ?comment. FILTER (langMatches(lang(?comment),"en"))}
        OPTIONAL {dbr:""" + ent + """ dct:description ?description. FILTER (langMatches(lang(?description),"en"))}
        }""")

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()

    return results


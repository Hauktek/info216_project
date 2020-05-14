from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON
import urllib

def enrich_data(entity):
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    ent = urllib.parse.quote(entity)
    ent = ent.replace(".","%2E")

    sparqlDB.setQuery("""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?label ?comment ?description
        WHERE { 
        OPTIONAL {dbr:""" + ent + """ rdfs:label ?label. FILTER (langMatches(lang(?label),"en"))}
        OPTIONAL {dbr:""" + ent + """ rdfs:comment ?comment. FILTER (langMatches(lang(?comment),"en"))}
        OPTIONAL {dbr:""" + ent + """ dct:description ?description. FILTER (langMatches(lang(?description),"en"))}
        }""")

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()

    return results



def find_types(entity):
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    ent = urllib.parse.quote(entity)
    ent = ent.replace(".","%2E")

    sparqlDB.setQuery("""
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?x
        WHERE { dbr:""" + ent + """ a ?x.
        
        }""")

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()

    return results

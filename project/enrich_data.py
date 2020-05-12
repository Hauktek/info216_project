from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON
import urllib

def enrich_data(entity):
    sparqlDB = SPARQLWrapper("http://dbpedia.org/sparql")

    prefixDBR = "PREFIX dbr: <http://dbpedia.org/resource/> "
    prefixRDFS = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
    prefixDCT = "PREFIX dct: <http://purl.org/dc/terms/> "
    prefixDBO = "PREFIX dbo: <http://dbpedia.org/ontology/> "
    prefixDBP = "PREFIX dbp: <http://dbpedia.org/property/>"

    ent = urllib.parse.quote(entity)
    ent = ent.replace(".","%2E")

    sparqlDB.setQuery("""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT ?label ?comment ?description
    WHERE { dbr:""" 
    + ent + 
    """ rdfs:label ?label;
    rdfs:comment ?comment;
    dct:description ?description.
    FILTER (langMatches(lang(?label),"en"))
    FILTER (langMatches(lang(?description),"en"))
    FILTER (langMatches(lang(?comment),"en"))
    }
    """)

    sparqlDB.setReturnFormat(JSON)
    results = sparqlDB.query().convert()

    return results



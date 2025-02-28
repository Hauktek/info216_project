from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD, RDFS
from rdflib.collection import Collection
import json
import pycountry
import urllib
import requests
from enrich_data import find_data
from blaze_setup import blaze_uploader

g = Graph()

# Declaration of namespaces
ex = Namespace('http://example.org/')
schema = Namespace('https://schema.org/')
dbr = Namespace('http://dbpedia.org/resource/')
wiki = Namespace('https://www.wikidata.org/wiki/')
dct = Namespace('http://purl.org/dc/terms/')
foaf = Namespace('http://xmlns.com/foaf/0.1/')

# Binding of namespaces to prefixes
g.bind('ex', ex)
g.bind('schema', schema)
g.bind('dbr', dbr)
g.bind('foaf', foaf)
g.bind('wiki', wiki)
g.bind('dct', dct)

# Load the json data from webhose and put it in a variable 
with open('webhoseData.json', encoding="utf8") as json_file:
    data = json.load(json_file)

# A function for making a API call to dbpedia spotlight for named entity linking.
# Takes one argument of text and returns text and entities in json format.
def spotlightCall(text):
    text_call = urllib.parse.quote(text)
    response = requests.get('http://api.dbpedia-spotlight.org/en/annotate?text=' + text_call, headers={'Accept':'application/json'},)
    return response

# A fuction for creating triples from data and adding them to a graph
# Takes one argument of data 
def graph_setup(data):
    g.add((ex.Entity, RDF.type, RDFS.Class))
    g.add((ex.hasEntity, RDFS.range, ex.Entity))
    g.add((ex.hasEntity, RDFS.domain, schema.NewsArticle))

    entityData = []

    # Iterates through each article data, makes an API call to dbpedia spotlight for entity extraction and creates triples from the metadata and entities.
    for article in data['posts']:
        thread = article['thread']
        subject = article['uuid']

        response = spotlightCall(article['text'])
        
        # If the API request is ok, then it makes triples out of entities and metadata
        if response.status_code == 200:
            for res in response.json()["Resources"]:
                # Checks if the resource have @types to find out if it is a valid resource
                if res["@types"]:
                    # Parses the dbpedia resource to a string with valid characters and adds it as an object
                    ent = res["@URI"].split('/resource/')
                    obj = urllib.parse.quote(ent[1])
                    g.add((URIRef(ex + subject), ex.hasEntity, URIRef(dbr + obj)))

                    # If entity-data not already added to the graph, "enrich_data.py" queries dbpedia and retrieves entity-types, label, comment and description.  
                    if ent[1] not in entityData: 
                        entityData.append(ent[1])
                        results = find_data(ent[1])
                        for result in results["results"]["bindings"]:
                            if 'http://dbpedia.org/ontology/' in result['type']['value']:
                                dbType = result['type']['value'].split('http://dbpedia.org/ontology/')
                                g.add((URIRef(dbr + obj), RDF.type, URIRef(dbr + dbType[1])))
                            if 'http://xmlns.com/foaf/0.1/' in result['type']['value']:
                                foafType = result['type']['value'].split('http://xmlns.com/foaf/0.1/')
                                g.add((URIRef(dbr + obj), RDF.type, URIRef(foaf + foafType[1])))
                            if 'label' in result:
                                g.add((URIRef(dbr + obj), RDFS.label, Literal(result["label"]["value"], datatype=XSD.string)))
                            if 'comment' in result:
                                g.add((URIRef(dbr + obj), RDFS.comment, Literal(result["comment"]["value"], datatype=XSD.string)))
                            if 'description' in result:
                                g.add((URIRef(dbr + obj), dct.description, Literal(result["description"]["value"], datatype=XSD.string)))
                        
                    # Uses the metadata provided from webhose to create triples
                    g.add((URIRef(ex + subject), RDF.type, schema.NewsArticle))

                    g.add((URIRef(ex + subject), RDFS.label, Literal(thread['title_full'], datatype=XSD.string)))

                    g.add((URIRef(ex + subject), schema.headline, Literal(thread['title_full'], datatype=XSD.string)))     

                    g.add((URIRef(ex + subject), schema.url, Literal(thread['url'], datatype=XSD.anyURI)))                  

                    g.add((URIRef(ex + subject), schema.articleBody, Literal(article['text'], datatype=XSD.string)))

                    g.add((URIRef(ex + subject), schema.datePublished, Literal(thread['published'], datatype=XSD.dateTime)))

                    g.add((URIRef(ex + subject), schema.wordCount, Literal(len(article['text'].split()), datatype=XSD.integer)))

                    if article['author'] != '':
                        g.add((URIRef(ex + subject), schema.author, Literal(article['author'], datatype=XSD.string))) 
                    
                    # Creates triples with dbpedia resource out of country and language metadata by manipulating the data.
                    # This wont always create a valid resource. 
                    if thread['country'] != '':
                        country = pycountry.countries.get(alpha_2=thread['country'])
                        country = country.name.replace(" ", "_")
                        g.add((URIRef(ex + subject), schema.countryOfOrigin, URIRef(dbr + country)))
                        g.add((URIRef(dbr + country), RDF.type, dbr.PopulatedPlace))
                        g.add((URIRef(dbr + country), RDF.type, dbr.Place))
                        g.add((URIRef(dbr + country), RDF.type, dbr.Location))
                        g.add((URIRef(dbr + country), RDF.type, dbr.Country))
                        g.add((URIRef(dbr + country), RDF.type, wiki.Q6256))
                        g.add((URIRef(dbr + country), RDF.type, wiki.Q315))
                        g.add((URIRef(dbr + country), RDF.type, schema.Place))
                        g.add((URIRef(dbr + country), RDF.type, schema.Country))

                    if article['language'] != '':
                        language = article['language'].capitalize()
                        g.add((URIRef(dbr + language), RDF.type, dbr.Language))
                        g.add((URIRef(ex + subject), schema.inLanguage, URIRef(dbr + language)))    
                        g.add((URIRef(dbr + language), RDF.type, wiki.Q34770))
                        g.add((URIRef(dbr + language), RDF.type, wiki.Q315))
                        g.add((URIRef(dbr + language), RDF.type, schema.Language))     


# Run the function to set up the graph with triples from json data
graph_setup(data)

# Prints the graph in turtle format
print(g.serialize(format="turtle").decode())

# Write the graph to a file in turtle format 
g.serialize(destination="triples.ttl", format="turtle")   

# Upload the turtle file to blazegraph
blaze_uploader()
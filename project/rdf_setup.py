from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import RDF, FOAF, XSD, RDFS
from rdflib.collection import Collection
import json
import pycountry
import urllib
import requests
import time
from time_finder import Finder
from text_analyzer import Analyzer

g = Graph()

ex = Namespace('http://example.org/')
schema = Namespace('https://schema.org/')
dbp = Namespace('https://dbpedia.org/resource/')
wiki = Namespace('https://www.wikidata.org/wiki/')

g.bind('ex', ex)
g.bind('schema', schema)
g.bind('dbp', dbp)
g.bind('foaf', FOAF)
g.bind('wiki', wiki)

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
def makeTriples(data):
    # Iterates through each article data and set up time and text analyzers, and makes an API call to dbpedia spotlight
    for article in data['posts']:
        thread = article['thread']
        subject = article['uuid']

        timeFinder = Finder(thread['published'])
        textAnalyzer = Analyzer(article['text'])
        response = spotlightCall(article['text'])
        
        # If the API request is ok, then it makes triples out of entities and metadata
        if response.status_code == 200:
            for res in response.json()["Resources"]:
                # Checks if the resource have @types to find out if it is a valid resource
                if res["@types"]:
                    # Parses the dbpedia resource to a string with valid characters and adds it an object
                    ent = res["@URI"].split('/resource/')
                    obj = urllib.parse.quote(ent[1])
                    g.add((URIRef(ex + subject), ex.hasEntity, URIRef(dbp + obj)))

                    # Iterates through types and creates triples based on the type of types. 
                    types = res["@types"].split(',')
                    for t in types:
                        t_split = t.split(':')
                        if t_split[0] == 'DBpedia':
                            g.add((URIRef(dbp + str(ent[1])), RDF.type, URIRef(dbp + t_split[1])))
                        if t_split[0] == 'Wikidata':
                            g.add((URIRef(dbp + str(ent[1])), RDF.type, URIRef(wiki + t_split[1])))
                        if t_split[0] == 'Schema':
                            g.add((URIRef(dbp + str(ent[1])), RDF.type, URIRef(schema + t_split[1])))

                    # Uses the metadata provided from webhose to create triples 
                    g.add((URIRef(ex + subject), RDF.type, schema.NewsArticle))

                    if thread['title_full'] != '':
                        g.add((URIRef(ex + subject), RDFS.label, Literal(thread['title_full'], datatype=XSD.string)))
            
                    g.add((URIRef(ex + subject), schema.url, Literal(thread['url'], datatype=XSD.anyURI)))

                    if article['author'] != '':
                        g.add((URIRef(ex + subject), schema.author, Literal(article['author'], datatype=XSD.string)))
                    
                    if thread['title_full'] != '':
                        g.add((URIRef(ex + subject), schema.headline, Literal(thread['title_full'], datatype=XSD.string)))

                    g.add((URIRef(ex + subject), schema.articleBody, Literal(article['text'], datatype=XSD.string)))

                    for category in thread['site_categories']:
                        g.add((URIRef(ex + subject), ex.siteCategory, Literal(category)))
                    
                    g.add((URIRef(ex + subject), ex.sectionTitle, Literal(thread['section_title'], datatype=XSD.string)))
                    
                    # Creates triples with dbpedia resource out of country and language metadata by manipulating the data.
                    # This wont always create a valid resource. 
                    if thread['country'] != '':
                        country = pycountry.countries.get(alpha_2=thread['country'])
                        country = country.name.replace(" ", "_")
                        g.add((URIRef(ex + subject), schema.countryOfOrigin, URIRef(dbp + country)))
                        g.add((URIRef(dbp + country), RDF.type, dbp.PopulatedPlace))
                        g.add((URIRef(dbp + country), RDF.type, dbp.Place))
                        g.add((URIRef(dbp + country), RDF.type, dbp.Location))
                        g.add((URIRef(dbp + country), RDF.type, dbp.Country))
                        g.add((URIRef(dbp + country), RDF.type, wiki.Q6256))
                        g.add((URIRef(dbp + country), RDF.type, wiki.Q315))
                        g.add((URIRef(dbp + country), RDF.type, schema.Place))
                        g.add((URIRef(dbp + country), RDF.type, schema.Country))

                    if article['language'] != '':
                        language = article['language'].capitalize()
                        g.add((URIRef(dbp + language), RDF.type, dbp.Language))
                        g.add((URIRef(ex + subject), schema.inLanguage, URIRef(dbp + language)))    
                        g.add((URIRef(dbp + language), RDF.type, wiki.Q34770))
                        g.add((URIRef(dbp + language), RDF.type, wiki.Q315))
                        g.add((URIRef(dbp + language), RDF.type, schema.Language))

                    # Creates triples of the date and shows that it is possible to manipulate data to find more exact triples. (can be expanded to day/month names and more)
                    g.add((URIRef(ex + subject), schema.datePublished, Literal(thread['published'], datatype=XSD.dateTime)))
                    g.add((URIRef(ex + subject), ex.yearPublished, Literal(timeFinder.findYear(), datatype=XSD.gYear)))
                    g.add((URIRef(ex + subject), ex.monthPublished, Literal(timeFinder.findMonth(), datatype=XSD.gMonth)))
                    g.add((URIRef(ex + subject), ex.dayPublished, Literal(timeFinder.findDay(), datatype=XSD.gDay)))

                    # Creates triples from manipulation of the text tokens. Shows the possibility of creation of extra data. (can be expanded to other lexical properties)
                    g.add((URIRef(ex + subject), schema.wordCount, Literal(textAnalyzer.findWordCount(), datatype=XSD.integer)))
                    g.add((URIRef(ex + subject), ex.uniqueTypes, Literal(textAnalyzer.findUniqueTypes(), datatype=XSD.integer)))
                    g.add((URIRef(ex + subject), ex.typeTokenRatio, Literal(textAnalyzer.findTypeTokenRatio(), datatype=XSD.float)))



# Run the function to make triples from json data
makeTriples(data)

# Prints the graph in turtle format
print(g.serialize(format="turtle").decode())

# Write the graph to a file in turtle format 
g.serialize(destination="triples.ttl", format="turtle")   
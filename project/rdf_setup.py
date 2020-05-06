from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, FOAF, XSD, RDFS
import json
import pycountry
import urllib
import requests
import time
from time_finder import Finder
from text_analyzer import Analyzer

numOfArticles = 0

x = 1

def spotlightCall(text):
    text_call = urllib.parse.quote(text)
    response = requests.get('http://api.dbpedia-spotlight.org/en/annotate?text=' + text_call, headers={'Accept':'application/json'},)
    return response

g = Graph()

ex = Namespace('http://example.org/')
schema = Namespace('https://schema.org/')
dbp = Namespace('https://dbpedia.org/resource/')

g.bind('ex', ex)
g.bind('schema', schema)
g.bind('dbp', dbp)
g.bind('foaf', FOAF)


with open('webhoseData.json', encoding="utf8") as json_file:
    data = json.load(json_file)


for article in data['posts']:
    thread = article['thread']
    subject = article['uuid']

    timeFinder = Finder(thread['published'])
    textAnalyzer = Analyzer(article['text'])
    response = spotlightCall(article['text'])
    
    if response.status_code == 200:
        for res in response.json()["Resources"]:
            if res["@types"]:
                # types = x["@types"].split(',')
                b = res["@URI"].split('/resource/')
                g.add((URIRef(ex + subject), ex.hasEntity, URIRef(dbp + str(b[1]))))




            g.add((URIRef(ex + subject), RDF.type, schema.NewsArticle))

            if thread['title_full'] != '':
                g.add((URIRef(ex + subject), RDFS.label, Literal(thread['title_full'], datatype=XSD.string)))
    
            g.add((URIRef(ex + subject), schema.url, Literal(thread['url'], datatype=XSD.anyURI)))

            if article['author'] != '':
                g.add((URIRef(ex + subject), schema.author, Literal(article['author'], datatype=XSD.string)))
                        
            if thread['country'] != '':
                country = pycountry.countries.get(alpha_2=thread['country'])
                g.add((URIRef(ex + subject), schema.countryOfOrigin, URIRef(dbp + country.name.replace(" ", "_"))))

            if article['language'] != '':
                g.add((URIRef(ex + subject), schema.inLanguage, URIRef(dbp + article['language'].capitalize())))
                        
            g.add((URIRef(ex + subject), schema.datePublished, Literal(thread['published'], datatype=XSD.dateTime)))
            g.add((URIRef(ex + subject), ex.yearPublished, Literal(timeFinder.findYear(), datatype=XSD.gYear)))
            g.add((URIRef(ex + subject), ex.monthPublished, Literal(timeFinder.findMonth(), datatype=XSD.gMonth)))
            g.add((URIRef(ex + subject), ex.dayPublished, Literal(timeFinder.findDay(), datatype=XSD.gDay)))

            g.add((URIRef(ex + subject), schema.wordCount, Literal(textAnalyzer.findWordCount(), datatype=XSD.integer)))
            g.add((URIRef(ex + subject), ex.uniqueTypes, Literal(textAnalyzer.findUniqueTypes(), datatype=XSD.integer)))
            g.add((URIRef(ex + subject), ex.typeTokenRatio, Literal(textAnalyzer.findTypeTokenRatio(), datatype=XSD.float)))

            if thread['title_full'] != '':
                g.add((URIRef(ex + subject), schema.headline, Literal(thread['title_full'], datatype=XSD.string)))

            g.add((URIRef(ex + subject), schema.articleBody, Literal(article['text'], datatype=XSD.string)))

                        
            for category in thread['site_categories']:
                g.add((URIRef(ex + subject), ex.siteCategory, Literal(thread['site_categories'])))

            g.add((URIRef(ex + subject), ex.sectionTitle, Literal(thread['section_title'], datatype=XSD.string)))

        numOfArticles = numOfArticles + 1
            
 

print(g.serialize(format="turtle").decode())

g.serialize(destination="triples.ttl", format="turtle")

print(numOfArticles)


    
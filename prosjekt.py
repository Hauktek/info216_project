from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, FOAF, XSD
import json


g = Graph()
ex = Namespace('http://example.org/')
schema = Namespace('https://schema.org/')


with open('data/testJson.json', encoding="utf8") as json_file:
    data = json.load(json_file)


for article in data['posts']:
    thread = article['thread']
    subject = article['uuid']

    g.add((URIRef(ex + subject), RDF.type, ex.NewsArticle))

    g.add((URIRef(ex + subject), schema.URL, Literal(thread['url'], datatype=XSD.anyURI)))

    g.add((URIRef(ex + subject), schema.datePublished, Literal(thread['published'], datatype=XSD.dateTime)))
    g.add((schema.datePublished, schema.DataType, schema.DateTime))



    # g.add((URIRef(ex + subject), ex.site, Literal(thread['site_full'])))

    # for category in thread['site_categories']:
    #     g.add((URIRef(ex + subject), ex.category, Literal(thread['site_categories'])))

    # g.add((URIRef(ex + subject), ex.sectionTitle, Literal(thread['section_title'])))

    # g.add((Literal(thread['site_full']), ex.siteType, Literal(thread['site_type']) ))

    # if article['author'] != '':
    #     g.add((URIRef(ex + subject), schema.author, Literal(article['author'], datatype=XSD.string)))

    # if thread['title_full'] != '':
    #     g.add((URIRef(ex + subject), ex.title, Literal(thread['title_full'], datatype=XSD.string)))

    # if thread['country'] != '':
    #     g.add((URIRef(ex + subject), schema.countryOfOrigin, URIRef(ex + thread['country'])))

    # if article['language'] != '':
    #     g.add((URIRef(ex + subject), schema.language, URIRef(ex + article['language'])))

    # if len(article['entities']['locations']) > 0:
    #     for loc in article['entities']['locations']:
    #         g.add((URIRef(ex + subject), ex.location, Literal(loc['name'])))

    # if len(article['entities']['persons']) > 0:
    #     for loc in article['entities']['persons']:
    #         g.add((URIRef(ex + subject), ex.person, Literal(loc['name'])))

    # if len(article['entities']['organizations']) > 0:
    #     for org in article['entities']['organizations']:
    #         g.add((URIRef(ex + subject), ex.organization, Literal(org['name'])))


print(g.serialize(format="turtle").decode())


#g.serialize(destination="example.ttl", format="turtle")
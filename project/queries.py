from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON

namespace = "kb"
sparql = SPARQLWrapper("http://10.0.0.6:9999/blazegraph/namespace/"+ namespace + "/sparql")

# Find article headline, author, country of origin and word count, filter to find those with over 500 words and display in ascending order. 
def find_by_wordcount(wordcount):
    sparql.setQuery("""
        PREFIX schema: <https://schema.org/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?wordCount ?headline ?author ?countryOfOrigin 
        WHERE {
            ?s schema:wordCount ?wordCount;
               schema:headline ?headline;
               schema:author ?author;
               schema:countryOfOrigin ?country.
        FILTER (?wordCount > '""" + wordcount + """'^^xsd:integer) 
        SERVICE <http://dbpedia.org/sparql> {
            ?country rdfs:label ?countryOfOrigin.
            FILTER (langMatches(lang(?countryOfOrigin),"en"))}
        }ORDER BY ASC(?wordCount)""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print('-'*50)
        print("Headline: " + result["headline"]["value"])
        print("Author: " + result["author"]["value"])
        print("Country of origin: " + result["countryOfOrigin"]["value"])
        print("Number of words: " + result["wordCount"]["value"])
        

# Find articles and show what they are about (entities). 
def find_article_entities():
    sparql.setQuery("""
        PREFIX ex: <http://example.org/>
        PREFIX schema: <https://schema.org/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?headline ?entityLabel ?description WHERE {
        ?s schema:headline ?headline;
            ex:hasEntity ?entity.
        ?entity rdfs:label ?entityLabel;
                OPTIONAL{?entity dct:description ?description.}
        } ORDER BY ASC(?headline) 
        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    article = []

    for result in results["results"]["bindings"]:
        if result["headline"]["value"] not in article:
            article.append(result["headline"]["value"])
            print('-'*50)
            print("Article: " + result["headline"]["value"])

        if 'description' in result:
            print("About: " + result["entityLabel"]["value"] + " - " + result["description"]["value"])
        else: 
            print("About: " + result["entityLabel"]["value"])
        

# Find articles that are about persons and list the persons with their gender
def find_person_gender():
    sparql.setQuery("""
        PREFIX ex: <http://example.org/>
        PREFIX schema: <https://schema.org/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

        SELECT DISTINCT ?headline ?personLabel ?description ?gender WHERE {
        ?s ex:hasEntity ?entity;
            schema:headline ?headline.
        ?entity a ?type;
            rdfs:label ?personLabel;
            dct:description ?description.
        FILTER (?type = foaf:Person)
        SERVICE <http://dbpedia.org/sparql> {?entity foaf:gender ?gender.}   
        } ORDER BY ASC(?headline) 
        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    article = []
    persons = []

    for result in results["results"]["bindings"]:
        if result["headline"]["value"] not in article:
            article.append(result["headline"]["value"])
            print('-'*50)
            print("Article: " + result["headline"]["value"])
            persons = []
        if result["personLabel"]["value"] not in persons:
            persons.append(result["personLabel"]["value"])
            print("About person: " + result["personLabel"]["value"] + " (" + result["gender"]["value"] + ") - " + result["description"]["value"])



# Find entities, their comments and list articles that involves those entities
def find_entity_articles():
    sparql.setQuery("""
        PREFIX ex: <http://example.org/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?entityLabel ?comment ?article
        WHERE {
            ?s ex:hasEntity ?entity;
            rdfs:label ?article.
            ?entity rdfs:label ?entityLabel.
        
            SERVICE <http://dbpedia.org/sparql> {
                ?entity rdfs:comment ?comment.
                FILTER (langMatches(lang(?comment),"en"))}   
        } ORDER BY ASC(?entityLabel)
        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    entities = []
    for result in results["results"]["bindings"]:
        if result["entityLabel"]["value"] not in entities:
            entities.append(result["entityLabel"]["value"])
            print('-'*50)
            print("Entity: " + result["entityLabel"]["value"])
            print("Comment: " + result["comment"]["value"])
        print("Involved in article: " + result["article"]["value"])








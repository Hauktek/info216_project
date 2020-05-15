from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, RDFXML, JSON

namespace = "test"
sparql = SPARQLWrapper("http://10.0.0.6:9999/blazegraph/namespace/"+ namespace + "/sparql")

prefixDBR = "PREFIX dbr: <http://dbpedia.org/resource/> "
prefixRDFS = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
prefixDCT = "PREFIX dct: <http://purl.org/dc/terms/> "
prefixDBO = "PREFIX dbo: <http://dbpedia.org/ontology/> "
prefixDBP = "PREFIX dbp: <http://dbpedia.org/property/>"


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
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?headline ?personLabel ?gender 

WHERE {
  	?s ex:hasEntity ?entity;
       schema:headline ?headline.
  
  	?entity a ?type.
  	?entity rdfs:label ?personLabel.
  
  	FILTER(?type = foaf:Person)
  
    SERVICE <http://dbpedia.org/sparql> {
              ?entity foaf:gender ?gender.}
     
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
            print("About person: " + result["personLabel"]["value"] + " - " + result["gender"]["value"])


   
        







# ####################
# ## SPARQL queries ##
# ####################
# def movie_details(title):
#     user_title = title
#     res = g.query("""SELECT DISTINCT ?title ?rating ?year ?director ?genre
#                     WHERE {
#                     ?movie a mo:Movie .
#                     ?movie mo:title ?title .
#                     ?movie mo:title '"""+user_title+"""'^^xsd:string .
#                     ?movie dbo:rating ?rating .
#                     ?movie dct:created ?year .
#                     ?movie mo:hasDirector ?director .
#                     ?movie dbo:genre ?genre
#                     }
#                     """)
#     return list(res)

# #Query looking for all actor names, ordered alphabetically.
# def alldirectors_query():
#     res = g.query("""SELECT DISTINCT ?name
#                     WHERE {
#                     ?director a dbr:Film_Director .
#                     ?director foaf:name ?name
#                     }
#                     ORDER BY ASC(?name)
#                     """)
#     return list(res)

# #Query looking for all movie titles, ordered alphabetically.
# def alltitles_query():
#     res = g.query("""SELECT DISTINCT ?title 
#                      WHERE {
#                      ?movie a mo:Movie .
#                      ?movie mo:title ?title 
#                      }
#                      ORDER BY ASC(?title)
#                      """)
#     return list(res)

# # Query looking for all actor names, ordered alphabetically. 
# def allactors_query():
#     res = g.query("""SELECT DISTINCT ?name
#                      WHERE {
#                      ?actor a dbo:Actor .
#                      ?actor foaf:name ?name 
#                      }
#                      ORDER BY ASC(?name)
#                      """)
#     return list(res)


# # Query that finds all movies directed by specific director, ordered by highest rating. 
# def specific_query(rating,director):
#     user_rating = rating
#     user_director = director
#     res = g.query("""SELECT DISTINCT ?title ?director ?name ?rating
#                      WHERE {
#                      ?title a mo:Movie .
#                      ?title mo:hasDirector ?director .
#                      ?title mo:hasDirector '"""+user_director+"""' .
#                      ?title mo:title ?name .
#                      ?title dbo:rating ?rating .
#                      FILTER (?rating >= '"""+user_rating+"""'^^xsd:float) 
#                      }
#                      ORDER BY DESC(?rating)
#                      """) 
#     return list(res)

# def reccomendation_query(actor1,actor2,actor3):
#     user_actor_choice1 = actor1
#     user_actor_choice2 = actor2
#     user_actor_choice2 = actor3
#     res = g.query("""SELECT DISTINCT ?title ?rating ?genre ?description ?director (GROUP_CONCAT(distinct ?actor; separator = ", ") as ?actors)
#                     WHERE {
#                     ?movie mo:title ?title .  
#                     ?movie dbo:rating ?rating .
#                     ?movie dbo:genre ?genre .
#                     ?movie dc:description ?description .
#                     ?movie mo:hasDirector ?director .
#                     {
#                         ?movie mo:hasActor ?actor .
#                         ?movie mo:hasActor '"""+actor1+"""'
#                     }
#                     UNION
#                     {
#                         ?movie mo:hasActor ?actor .
#                         ?movie mo:hasActor '"""+actor2+"""'
#                     }
#                     FILTER(?rating >= "1"^^xsd:int)
#                     }
#                     GROUP BY ?title ?rating ?genre ?description ?director
#                     LIMIT 3
#                     """)
#     return list(res)   




from queries import find_article_entities, find_by_wordcount, find_person_gender, find_entity_articles


# A simple function to present some example SPARQL queries
def app():
    print('-'*50)
    print("1 - program")
    print("2 - program")
    print("3 - program")
    print("4 - program")
    print("5 - program")
    print("6 - program")
    print("7 - quit")
    print('-'*50)

    user_input  = input("Choose program: ")

    if(user_input == "1"):
        print("Running program 1")
        find_article_entities()
    if(user_input == "2"):
        print("Running program 2")
        wordcount_input = input("Input the minimum wordcount: ")
        if(wordcount_input.isdigit()):
            find_by_wordcount(wordcount_input)
        else:
            print("Not a digit")
    if(user_input == "3"):
        print("Running program 3")
        find_person_gender()
    if(user_input == "4"):
        print("Running program 4")
        find_entity_articles()
    if(user_input == "7"):
        return
    app()

app()





from queries import test2, find_by_wordcount


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
        test2()

    if(user_input == "2"):
        print("Running program 2")
        wordcount_input = input("Input the minimum wordcount: ")
        if(wordcount_input.isdigit()):
            find_by_wordcount(wordcount_input)
        else:
            print("Not a digit")

    if(user_input == "3"):
        print("Running program 3")

    if(user_input == "4"):
        print("Running program 4")

    if(user_input == "5"):
        print("Running program 5")

    if(user_input == "6"):
        print("Running program 6")
        
    if(user_input == "7"):
        return

    app()

app()





# A class for retrieving extra data from text like number of words, nubber of unique words and type token ratio. 
# Used to show that it it possible to find extra information that lies in the text. 
class Analyzer:

    def __init__(self, text):
        self.text = text
        self.tokens = text.split()

    # Finds the number of words in text
    def findWordCount(self):
        wordCount = len(self.tokens)
        return wordCount

    # Finds number of unique words
    # We get a list of unique tokens and then find the number of how many types there are
    def findUniqueTypes(self):
        types = []
        for w in self.tokens:
            if w not in types:
                types.append(w)
        uniqueTypes = len(types)
        return uniqueTypes

    # Finds the Type Token Ratio (TTR)
    # TTR estimates the degree of lexical diversity in a text.
    # A high TTR indicates that there is a greater lexical variety.
    def findTypeTokenRatio(self):   
        numberOfTokens = self.findWordCount()
        numberOfTypes = self.findUniqueTypes()
        typeTokenRatio = (numberOfTypes / numberOfTokens) * 100
        return round(typeTokenRatio, 2)

    
    


    
    



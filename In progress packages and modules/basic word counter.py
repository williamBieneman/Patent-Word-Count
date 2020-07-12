#Basic Word Counter, by William Bieneman, April 17 2020

print("Welcome to basic word counter!")
print("This program will count every word in the text you enter, and then sort them by frequency, excluding single use words.")

text = input("\n Please input your text below:\n") #Allows the user to input the text they want counted

#fixes the text to be all lowercase, and have no punctuation
fixed_text = text.lower()
punctuation = ['.',',','?','/','<','>',':',';','"',"'",'[',']','{','}',"\\",'|','!','@','#','$','%','^','&','*','(',')','-','_','+','=','~','`']
for i in punctuation:
    fixed_text=fixed_text.replace(i,'')
print(fixed_text)

#defines a list based on the text:
wordList = fixed_text.split(' ')
print(wordList)

length = len(wordList)
n=0
wordCounts=[]
countedWords=[]

#counts each word in the list
for n in range(0,length):
    word = wordList[n]
    if countedWords.count(word)==0:
        count = wordList.count(word)
        #print("There are ", count, " instances of the word \"", word, "\" in your text.")
        wordCounts.append((count,word))
        countedWords.append(word)

leastCounted = int(input("What would you like to be the minimum amount of uses to be recorded?\n"))

wordCounts.append((n,'total'))
wordCounts.sort(reverse=True)
mostCountedTuple = wordCounts[1]
mostCountedInt = mostCountedTuple[0]
for n in wordCounts:
    if n[0] > leastCounted:
        print(n)
        



#irrelevent but i'm a proud father
def lists_to_dict(keys,values,d={}):
    """Turns any two given lists into a dictionary."""
    for i in keys:
        for n in values:
            d[i]=n
            values.remove(n)
            break
    return d
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#TO PRIME TEXT, INPUT IT INTO THE FUNCTION "prime('''text''')"
def prime(text:str):
    text=text.replace('\n',' ')
    return text

print('\n\ndone')

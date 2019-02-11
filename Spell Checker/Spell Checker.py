# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 13:54:53 2018

@author: James
"""

import re

#open and read in the file containing bigram data
bigrams = open("bigrams.txt", "r")
bigrams = bigrams.read()
bigrams = bigrams.split("\n")
bigramList = []
bigramValues = []
for line in bigrams:
    bigramList.append(line)
for element in bigramList:
    value = re.split(r'\t+', element)
    bigramValues.append(value)
bigramValues.pop()
bigramTotal = 0
for line in bigramValues:
    bigramTotal = bigramTotal + int(line[0])


# Create the four cost matrices by reading in the data and putting it in a list of lists
delete = open("deletion matrix.txt", "r")
delMatrix = []
delTotal = 0
for line in delete:
    number_strings = line.split()
    numbers = [n for n in number_strings] 
    delMatrix.append(numbers)
    for n in numbers:
        numba = int(n)
        delTotal = delTotal + numba

add = open("addition matrix.txt", "r")
addMatrix = []
addTotal = 0
for line in add:
    number_strings = line.split()
    numbers = [n for n in number_strings] 
    addMatrix.append(numbers)
    for n in numbers:
        numba = int(n)
        addTotal = addTotal + numba

sub = open("substitution matrix.txt", "r")
subMatrix = []
subTotal = 0
for line in sub:
    number_strings = line.split()
    numbers = [n for n in number_strings] 
    subMatrix.append(numbers)
    for n in numbers:
        numba = int(n)
        subTotal = subTotal + numba

rev = open("reversal matrix.txt", "r")
revMatrix = []
revTotal = 0
for line in rev:
    number_strings = line.split()
    numbers = [n for n in number_strings] 
    revMatrix.append(numbers)
    for n in numbers:
        numba = int(n)
        revTotal = revTotal + numba

#open and read in the english dictionary
dict = open("english3.txt", "r")
dict = dict.read()
correctList = []

#checks if a word is in the dictionary
def is_word(word):
    if word in dict:
        return True;
    else:
        return False;

#calculates the different possible edit distances for a word
def edit_distance(word):
    delete_distance(word)
    add_distance(word)
    sub_distance(word)
    rev_distance(word)

#calculates the delete distance for a word
def delete_distance(word):
    word = word.lower()
    letterCounter = -1
    #go through each character in the word
    for letter in word:
        letterCounter = letterCounter+1
        #split the word into a list of characters
        wordList = list(word)
        if letterCounter == 0:
            x = 26
        else:
            x = ord(wordList[letterCounter-1]) - 97
        y= ord(letter) - 97
        #delete a character from the word
        wordList.pop(letterCounter)
        #rejoin the list into a string
        wordString = "".join(wordList)
        #calculate edit distance
        chance = int(delMatrix[x][y]) / delTotal
        #if the word is in the dictionary, add to list of possible permutations
        if is_word(wordString) == True:
            correctList.append([wordString, chance])

#calculates the addition distance for a word         
def add_distance(word):
    word = word.lower()
    letterCounter = -1
    for letter in word:
        letterCounter = letterCounter + 1
        #same thing as del_distance, except add each letter into each possible position
        for i in range(26):
            wordList = list(word)
            if letterCounter == 0:
                x = 26
            else:
                x = ord(wordList[letterCounter-1]) - 97
            y = i
            wordList.insert(letterCounter, chr(97+i))
            wordString = "".join(wordList)
            #check if the word is in the dictionary
            if is_word(wordString) == True:
                chance = int(addMatrix[x][y]) / addTotal
                #if so, add to list of possible permutations
                correctList.append([wordString, chance])
    letterCounter= letterCounter + 1
    #calculate the weight from the addition matrix
    x = ord(wordList[letterCounter-1]) - 97
    for i in range(26):
        y = i
        wordList = list(word)
        wordList.insert(letterCounter, chr(97+i))
        wordString = "".join(wordList)
        if is_word(wordString) == True:
            chance = int(addMatrix[x][y]) / addTotal
            correctList.append([wordString, chance])

#calculates the substitution distance for a word     
def sub_distance(word):
    word = word.lower()
    letterCounter = -1
    #same thing, but substitute each letter for each position
    for letter in word:
        letterCounter = letterCounter+1
        wordList = list(word)
        x = ord(wordList[letterCounter]) - 97
        for i in range(26):
            y= i
            wordList[letterCounter] = chr(97+i)
            wordString = "".join(wordList)
            if is_word(wordString) == True:
                chance = int(subMatrix[x][y]) / addTotal
                correctList.append([wordString, chance])
    
#calculates the reversal distance for a word
def rev_distance(word):
    word = word.lower()
    wordList = list(word)
    #same thing, but switch adjacent letters and see if that is a word
    for i in range(len(wordList)-1):
        wordList = list(word)
        x = ord(wordList[i]) - 97
        y = ord(wordList[i+1]) - 97
        wordList[i], wordList[i+1] = wordList[i+1], wordList[i]
        wordString = "".join(wordList)
        if is_word(wordString) == True:
            chance = int(revMatrix[x][y]) / revTotal
            correctList.append([wordString, chance])

#calculates the best replacement word for a word that is not in the dictionary    
def best_word(given, current):
    total = 0
    #goes through bigrams and checks for the first (given) word
    for line in bigramValues:
        if line[1] == given:
            total = total + int(line[0])
    for line in bigramValues:
        if line[1] == given:
            #if the given matches, go through the list of possible new words and see if they match the next word
            for i in range(len(correctList)):
                if line[2] == correctList[i][0]:
                    #if they do, add the value to the chance of that word
                    chance = int(line[0]) / total
                    correctList[i][1] = correctList[i][1] + chance
                    
    bestWord = ""
    highValue = 0
    #pick the word with the highest chance of being correct
    for i in range(len(correctList)):
        if correctList[i][1] > highValue:
            highValue = correctList[i][1]
            bestWord = correctList[i][0]
    #add the word and the correction to the output list
    if bestWord == current:
        output.append(current)
        output.append(" ")
    else:
        output.append(current)
        output.append(" ")
        output.append("(" + bestWord + ")")    

#calculates the best replacement word for a word that is in the dictionary          
def check_word(given, current):
    global sentenceError
    global  sentenceContext
    total = 0
    for i in range(len(correctList)):
        correctList[i][1] = 0
    #goes through bigrams and checks for the first (given) word
    for line in bigramValues:
        if line[1] == given:
            total = total + int(line[0])
    for line in bigramValues:
        if line[1] == given:
            #if the given matches, go through the list of possible new words and see if they match the next word
            for i in range(len(correctList)):
                if line[2] == correctList[i][0]:
                    #if they do, add the value to the chance of that word
                    chance = int(line[0])/total
                    correctList[i][1] = correctList[i][1] + chance
    bestWord = ""
    highValue = 0
    #pick the word with the highest chance of being correct
    for i in range(len(correctList)):
        if correctList[i][1] > highValue:
            highValue = correctList[i][1]
            bestWord = correctList[i][0]
    if highValue == 0:
        bestWord = correctList[0][0]
    if bestWord == current:
        output.append(current)
    else:
        #add the word and the correction to the output list
        output.append(current)
        #if there have been no corrections in this sentence, add the correction to the output file
        if sentenceError == 0 and sentenceContext == 0:
            output.append(" ")
            output.append("(" + bestWord + ")")
            sentenceContext = sentenceContext + 1

#read in the file and split into a list of everything and a list of just the words   
#fileName = input("Please enter the name of the file \n")
fileName = "spell_input.txt"
data= open(fileName, "r")
data= data.read()
punctuation = re.findall(r"[\w']+|[.,!?;]", data)
data=re.sub(r'\W+', ' ', data)
data = data.replace("\n", " ")
data=data.split(' ')

output = []
sentenceContext = 0
sentenceError = 0
#go through the list of everything
for i in punctuation:
    #check if the element is a word
    if i in data:
        index = data.index(i)
        word = data[index]
        #check if the word is capitalized but not the beginning of a sentence. If it is, assume it is spelled correctly
        if word[0].isupper() == True and data[index-1] != "." and data[index-2] != "." and data[index-1] != "!" and data[index-2] != "!" and data[index-1] != "?" and data[index-2] != "?":
            output.append(i)
            output.append(" ")
        #check if the word is in the dictionary
        elif is_word(i.lower()) == False:
            if i.isdigit() == False:
                #calculate all the possible permutations with edit_distance
                 edit_distance(i)
                 #calculate the best replacement word given the current word and the one before it
                 best_word(data[index-1], i)
                 sentenceError = sentenceError + 1
                 correctList = []
            else:
                output.append(i)
                output.append(" ")
        else:
            #else is for words that are in the dictionary
            if i.isdigit() == False:
                #add the word to the list of possible correct words
                correctList.append([i, 0])
                #calculate possible permutations with edit distance
                edit_distance(i)
                #determine if a replacement word is necessary or if the given word is the best choice
                check_word(data[index-1], i)
                output.append(" ")
                correctList = []
    else:
        #if the last element is a sentence delimiter, reset the error counters because a new sentence is starting
        if i == '.' or i == '!' or i == '?':
            sentenceContext = 0
            sentenceError = 0
        output.pop()
        output.append(i)
        output.append(" ")
            
                
        
#write results to file
outputFile= open("output.txt","w+")

for i in output:
    outputFile.write(i)
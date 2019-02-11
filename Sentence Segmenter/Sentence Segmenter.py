# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 14:31:41 2018

@author: James
"""

#list of common abbreviations
abbreviations = ["mr.", "mrs.", "ms.", "dr.", "st.", "e.g.", "i.e.", "jr.", "sr.", "vs.", "ph.d.", "mt.", "p.s.", "a.s.a.p.", "d.i.y."]
#variables
sentenceNum = 1
sentence = ""
sentenceList = []
closedQuote = True





#read in the input file, remove new lines, split based on spaces
#data= open("test_input3.txt", "r")
data= open("input.txt", "r")
data= data.read()
data = data.replace("\n", " ")
data=data.split(' ')




#segmentSentences function takes in a list of words, combines them into sentences, and adds those sentences to sentenceList 
def segmentSentences(words):
    global sentence
    global closedQuote
    #loop through each word in the input file
    for i in words:
        #bool closedQuote is only false when there is an opening quotation mark, but not a closing one
        if('"' in i):
            closedQuote = not closedQuote
        # this if is for words that contain the end of a quotation
        if(closedQuote == True and '"' in i):
            #if the word doesn't contain a sentence terminator, keep adding to the sentence
            if('.' not in i and '?' not in i and '!' not in i):
                sentence = sentence + i + " "
            #if it contains a terminator, check if the next word is capitalized. If it is, start a new sentence. If not, don't end the sentence
            elif('?' in i or '!' in i):
                index = words.index(i)
                next = words[index+1]
                if(next[1].isupper()):
                    sentence = sentence + i
                    sentenceList.append(sentence)
                    sentence = ""
                else:
                    sentence = sentence + i + " "
            #if the word contains a period, check if it's an abbreviation
            elif('.' in i):
              #  print(i)
                if(i.lower() in abbreviations):
                    sentence = sentence + i + " "
                #check if the next word is capitalized
                else:
                    index = words.index(i)
                    next = words[index+1]
                    if(next[0].isupper()):
                        sentence = sentence + i
                        sentenceList.append(sentence)
                        sentence = ""
                    else:
                        sentence = sentence + i + " "
        #the else is for words that don't contain the end of a quotation           
        else:
            if('.' not in i and '?' not in i and '!' not in i):
                sentence = sentence + i + " "
            elif('?' in i or '!' in i):
                sentence = sentence + i
                sentenceList.append(sentence)
                sentence = ""
            else:
                 #check if the word is in the list of common abbreviations. If it is, don't end the sentence.
                if(i.lower() in abbreviations):
                    sentence = sentence + i + " "
                #if the last character isn't a period, it is probably a number or abbreviation, so don't end the sentence
                elif(i[-1] != '.'):
                    sentence = sentence + i + " "
                #otherwise, end the sentence and start a new one
                else:
                    sentence = sentence + i
                    sentenceList.append(sentence)
                    sentence = ""
            
#create new file to write the output to
outputFile= open("output.txt","w+")


#call the function
segmentSentences(data)

#write the segmented sentences to output.txt
for i in sentenceList:
    #some sentences have extra space at the front due to replacing new line with a space. This checks for that and removes the extra space if it exists.
    if(i[0] == " "):
        outputFile.write(str(sentenceNum) + ": " + i[1:] + '\n')
    else:
        outputFile.write(str(sentenceNum) + ": " + i + '\n')
    sentenceNum += 1
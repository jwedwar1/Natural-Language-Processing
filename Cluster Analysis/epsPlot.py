# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 17:54:53 2018

@author: James
"""

import os
import re
import math
import matplotlib.pyplot as mplot

documentList = []
corpus = []
logFreqList = []
finalClusterList = []



for filename in os.listdir(r'C:\Users\James\Part1'):
#for filename in os.listdir(r'C:\Users\James\cluster'):
    #print(count)

    data = open(filename, "r")
    data = data.read()
    data=re.sub(r'\W+', ' ', data)
    data = data.lower()
    data = data.split(' ')
    data.pop()
    documentList.append(data)

print("all docs read in")
# fills the corpus with each unique term
for i in range(len(documentList)):
    for j in range(len(documentList[i])):
        if documentList[i][j] not in corpus:
            corpus.append(documentList[i][j])
            
print("all unique terms")
#make an array for each document that is the same length as the corpus
#fill the array with the counts that each term appears in the document
count = 0
for i in range(len(documentList)):
#    print(count)
    doc = documentList[i]
    docTC = [0] * len(corpus)
    for word in doc:
        index = corpus.index(word)
        docTC[index] = docTC[index] + 1
    
    for j in range(len(docTC)):
        if docTC[j] != 0:
            docTC[j] = 1 + math.log10(docTC[j])
    
    logFreqList.append(docTC) 
    count = count + 1


#returns the similarity of two documents
def cos_sim(a, b):
    sum = 0
    for i in range(len(a)):
        sum = sum + (a[i] * b[i])
    return sum

# get the k nearest neighbors
#get the distance
#add the distance of the k nearest neighbor to a list
# sort the list and graph it

pointList = []

for i in range(len(logFreqList)):
    pointDistances = []
    for j in range(len(logFreqList)):
        if (j != i):
            similarity = cos_sim(logFreqList[i], logFreqList[j])
            pointDistances.append(similarity)
    #sort the distances in pointDistances
    pointDistances.sort()
    pointList.append(pointDistances)

#add the similarities to a list to be graphed
graphList = []
k = 4
for i in range(len(pointList)):
    similarity = pointList[i][k-1]
    graphList.append(similarity)
    
graphList.sort()
mplot.xlabel("points sorted according to distance of 4th nearest neighbor")
mplot.ylabel("4th nearest neighbor cos similarity")
mplot.scatter(range(len(pointList)), graphList)
mplot.plot(range(len(pointList)), graphList)
mplot.show()
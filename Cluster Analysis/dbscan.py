# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 17:54:53 2018

@author: James
"""

import os
import re
import math
import pickle

#documentList = pickle.load( open( "documentList.p", "rb" ) )
#corpus = pickle.load( open( "corpus.p", "rb" ) )
#logFreqList = pickle.load( open( "logFreqList.p", "rb" ) )
#finalClusterList = []
documentList = []
corpus = []
logFreqList = []
finalClusterList = []




for filename in os.listdir(r'C:\Users\James\Part1'):
    data = open(filename, "r")
    data = data.read()
    data=re.sub(r'\W+', ' ', data)
    data = data.lower()
    data = data.split(' ')
    data.pop()
    documentList.append(data)


# fills the corpus with each unique term
for i in range(len(documentList)):
    for j in range(len(documentList[i])):
        if documentList[i][j] not in corpus:
            corpus.append(documentList[i][j])
            

#make an array for each document that is the same length as the corpus
#fill the array with the counts that each term appears in the document

for i in range(len(documentList)):
    doc = documentList[i]
    docTC = [0] * len(corpus)
    for word in doc:
        index = corpus.index(word)
        docTC[index] = docTC[index] + 1
    
    for j in range(len(docTC)):
        if docTC[j] != 0:
            docTC[j] = 1 + math.log10(docTC[j])
    
    logFreqList.append(docTC)  



#returns the similarity of two documents
def cos_sim(a, b):
    sum = 0
    for i in range(len(a)):
        sum = sum + (a[i] * b[i])
    return sum

#calculates the average point of a cluster
def cal_avg(c):
    avg = [0] * len(corpus)
    # go through each word in the document
    for i in range(len(avg)):
        sum = 0
        # go through each document in the cluster
        for j in range(len(c)):
            sum = sum + c[j][i]
        ind_avg = sum / (len(c))
        avg[i] = ind_avg
    return avg


pcList = []
 

#value gotten from epsPlot graph
minDistance = 40

#go through all the points and get rid of the noise points
for i in range(len(logFreqList)):
    pointDistances = []
    for j in range(len(logFreqList)):
        #if it's not the same point
        if (j != i):
            dist = cos_sim(logFreqList[i], logFreqList[j])
            pointDistances.append(dist)
    #sort the distances in pointDistances
    pointDistances.sort()
    
    

    #k is the 4th farthest element
    k = 3
    
    #check if the kth element of the pointDistances list is less than whatever the minimum is
    #if it is, it's not a noise point, so add to the pcList
    if(pointDistances[k] > minDistance):
        pcList.append([[],logFreqList[i]])
    
print("noise points removed")

    
current_cluster_label = 0
#for all core points
for i in range(len(pcList)):
    #if the core point has no cluster label, increment current_cluster_label by 1
    if(pcList[i][0] == []):
        current_cluster_label = current_cluster_label + 1
        pcList[i][0] = [current_cluster_label]
    #for all points in the minDistance neighborhood, except for the point itself,
    #if the point doesn't have a cluster label, label it with current_cluster_label
    for j in range(len(pcList)):
        if(j != i):
            if(pcList[j][0] == []):
                dist = cos_sim(pcList[i][1], pcList[j][1])
                if(dist >= 70):
                    pcList[j][0] = [current_cluster_label]

#find out number of clusters  
maxGroupNum = 0 
for i in range(len(pcList)):
    if(pcList[i][0][0] > maxGroupNum):
        maxGroupNum = pcList[i][0][0]

#add the correct number of empty clusters to the list
finalClusterList = []
for i in range(maxGroupNum):
    finalClusterList.append([])

#fill the finalClusterList with the points belonging to each cluster
for i in range(maxGroupNum):
    for j in range(len(pcList)):
        if(pcList[j][0] == [i+1]):
            finalClusterList[i].append(pcList[j][1])

sse_sum = 0
#using cosine similarity, so bigger number is best
for i in range(len(finalClusterList)):
    mean = cal_avg(finalClusterList[i])
    #go through each point in the cluster
    for j in range(len(finalClusterList[i])):
        dist = cos_sim(mean, finalClusterList[i][j])
        sse_sum = sse_sum + dist
print("there are this many groups: ", maxGroupNum)
print("kmeans sse is: ")
print(sse_sum)
            
        
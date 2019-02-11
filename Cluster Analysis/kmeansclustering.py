# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:53:48 2018

@author: James
"""
import os
import re
import math
import random



#documentList = pickle.load( open( "documentList.p", "rb" ) )
#corpus = pickle.load( open( "corpus.p", "rb" ) )
#logFreqList = pickle.load( open( "logFreqList.p", "rb" ) )
#finalClusterList = []

#klist = [15]
klist = [5,7,10,12,15]
documentList = []
corpus = []
logFreqList = []
finalClusterList = []

count = 0

#read in the files and convert them to bag of words
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
    count = count + 1

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
            #normalize the term counts
            docTC[j] = 1 + math.log10(docTC[j])
    
    logFreqList.append(docTC)

#returns the similarity of two documents
def cos_sim(a, b):
    sum = 0
    for i in range(len(a)):
        sum = sum + (a[i] * b[i])
    return sum

#returns k random indices to be the starting center of the clusters
def random_points(k):
    count = 0
    centerPoints = []
    pointList = list(range(len(documentList)))
    while(count < k):
        point = random.choice(pointList)
        centerPoints.append(point)
        #makes sure it doesn't choose the same point twice
        pointList.remove(point)
        count = count + 1
    return centerPoints

#calculates the average point (centroid) of a cluster c
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

#method to assign every point to the nearest cluster
def assign_points():
    for i in range(len(logFreqList)):
        maxSimilarity = 0
        clusterIndex = 0
        for j in range(len(midPoints)):
            if cos_sim(logFreqList[i], midPoints[j]) > maxSimilarity:
                maxSimilarity = cos_sim(logFreqList[i], midPoints[j])
                clusterIndex = j
                clusters[clusterIndex].append(logFreqList[i])

#method to calculate the average of every cluster
def avg_all_clusters():
    for i in range(len(midPoints)):
        midPoints[i] = cal_avg(clusters[i])
    
#for each k
for knum in klist:
    #generates random starting midpoints
    randomMidIndices = random_points(knum)
    midPoints = []
    clusters = []
    count = 0
    #adds the correct number of empty clusters to the clusters list
    while(count < knum):
        clusters.append([])
        count = count + 1
    # 1- however many clusters
    # puts the correct starting points in the midPoints list
    for i in range(knum):
        midPoints.append(logFreqList[randomMidIndices[i]])
    #assign all the points to the nearest cluster
    assign_points()
    #get the previous average
    old_avg = midPoints
    #get a new average
    avg_all_clusters()
    wcount = 0
    while(old_avg != midPoints or wcount < 15):
        #number of repetitions
        print(wcount)
        #reassign points to the new midpoints
        assign_points()
        old_avg = midPoints
        avg_all_clusters()
        wcount = wcount + 1
    finalClusterList.append(clusters)
    
#calculate sse
sim_sum = 0
#go through each cluster
for i in range(len(finalClusterList[0])):
    #get the average
    mean = cal_avg(finalClusterList[0][i])
    for j in range(len(finalClusterList[0][i])):
        #sum the similarity between each point and the average point
        dist = cos_sim(mean, finalClusterList[0][i][j])
        sim_sum = sim_sum + dist

print("k: ", klist)
print("sse_sum: ", sim_sum)
    
    
    
#NOTE: this is the sum of sse for all k. In order to compare to dbscan, will probably want to calculate the sse for each
# k clusters and use the best one to compare with dbscan.
        
        
    
    
    
    
        
        
    
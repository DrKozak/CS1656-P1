#pinepy-search.py 

import argparse
import collections
import csv
import json
import glob
import math
import nltk 
import os
import pandas
import re
import requests
import string
import sys
import time
import xml

directory = os.getcwd() + '/input'


f = open('inverted-index.json','rb')
dictionary = {}
dictionary = json.load(f)
f.close()


stemArray = []
weight = {}

keywords = open("keywords.txt").readlines()


#for loop adjusts the keywords and gathers the weights for the alg
for file_input in os.listdir(directory):
     if not file_input.startswith('.'):


        for i in keywords:

            
            phrase = i.split(' ')
            for j in phrase :
                
                zeze = j.lower()
                
                
                regex = '''!()-[]{};:'"\\,<>./?@#$%^&\n*_~1234567890'''
                    
                    
                invalid_regex = ""
                for char in zeze:
                   if char not in regex:
                       invalid_regex = invalid_regex + char
                
                not_int = ''.join([i for i in invalid_regex if not i.isdigit()])
                
                tokenizer = nltk.word_tokenize(not_int)
                #Stemming process with nltk
                port = nltk.PorterStemmer()
                for token in tokenizer:
                        tokenizer = port.stem(token)

                if tokenizer not in stemArray:
                    
                    if tokenizer in dictionary:
                        if file_input in dictionary[tokenizer]:
                            n = dictionary[tokenizer]['count_times']
                            N = dictionary[tokenizer]['total'] #total num of docs
                            frequency = dictionary[tokenizer][file_input]

                            weightMath = ((1+math.log(float(frequency),2))*math.log(float(N)/n,2))
#       w(key, doc) = (1 + log2 frequency(key,doc)) * log2 (N / n(doc))
#   where n(doc) is the number of documents that contain keyword key and 
#   N is the total number of documents                     
                            if j not in weight:
                                weight[j] = {file_input:weightMath}
                            else:
                                weight[j][file_input] = weightMath
                    

weighted = {}

#for loop sums weights of diff docs if keywords are more than one
for i in keywords:
    
    phrase = i.split(' ')
    for j in phrase :
        for file_input in os.listdir(directory):
            if not file_input.startswith('.'):


                if j in weight:
                    if file_input in weight[j]:
                        if i not in weighted:
                            weighted[i] = {file_input:weight[j][file_input]}
                        else:
                            if file_input not in weighted[i]:
                                weighted[i][file_input] = weight[j][file_input]
                            else:
                                weighted[i][file_input] = weighted[i][file_input] + weight[j][file_input]
                    



#print the output
for i in keywords:
    
    print('------------------------------------------------------------')
    print ("\nKeywords =",i.lower())
    previous = -1
    counter = 0
    for k in (weighted[i]):
        cut_word = (max(weighted[i], key=weighted[i].get))
        if previous != weighted[i][cut_word]:
            counter = counter + 1
            previous = weighted[i][cut_word]
        
        
        
        print ("\n[%d]  File=%s  score=%.6f" % (counter,cut_word,weighted[i][cut_word]))
        weighted[i][cut_word] = 0  
        phrase = i.split(' ')
        for j in phrase:
            strip_string = j.strip("\n")
            if cut_word in weight[j]:
                print ("weight(%s): %.6f" % (strip_string.lower(), weight[j][cut_word]))
            else:
                print ("weight(%s): %.6f" % (strip_string.lower(), 0.0))
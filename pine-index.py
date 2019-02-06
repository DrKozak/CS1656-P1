#pine-index.py

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
#nltk.download('punkt')


count_times = 1
directory = os.getcwd() + '/input'
dictionary = {}
lists = []
for file_input in os.listdir(directory):
     if not file_input.startswith('.'):
        if file_input in lists:
            print('This document has been previously entered')
        else:
            
            
 #adjust words for the form to take into file           
            lists.append(file_input)
            count_times= count_times+1
        
            with open(os.path.join(directory, file_input) ,"r+") as f:
                zeze = f.read()
                zeze = zeze.lower()
                regex = '''!()-[]{};:'"\\,<>./?@#$%^&\n*_~1234567890'''
            
            
            invalid_regex = ""
            for char in zeze:
               if char not in regex:
                   invalid_regex = invalid_regex + char #not valid string
            
            
            
            not_int = ''.join([i for i in invalid_regex if not i.isdigit()])
            
            
            tokenizer = nltk.word_tokenize(not_int)
            #Stemming process happens here with nltk
            port = nltk.PorterStemmer()
            iterator = 0
            for token in tokenizer:
                    tokenizer[iterator] = port.stem(token)
                    iterator += 1       
            iterator = 0
            
            #for loop creates dictionary 
            for token in tokenizer:
                    if tokenizer[iterator] in dictionary:
                        if file_input in dictionary[tokenizer[iterator]]:
                            dictionary[tokenizer[iterator]][file_input] = dictionary[tokenizer[iterator]][file_input]+1
                        else:
                            dictionary[tokenizer[iterator]][file_input] = 1
                            dictionary[tokenizer[iterator]]['count_times'] = dictionary[tokenizer[iterator]]['count_times'] +1
                            dictionary[tokenizer[iterator]]['total'] = len(os.listdir(directory))
    
                        
                    
                    if tokenizer[iterator] not in dictionary:
                        
                        dictionary[tokenizer[iterator]] = {file_input: 1, 'count_times':1, 'total':(len(os.listdir(directory)))}
            
                        
                    iterator += 1
        

#Output to inverted-index.json
f = open('inverted-index.json','w')
json.dump(dictionary,f)
f.close()
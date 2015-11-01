#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,pickle,codecs
from wordnik import *
from random import Random

apiUrl = 'http://api.wordnik.com/v4'
apiKey = os.environ.get('API_KEY')
username = os.environ.get('USER_NAME')
password = os.environ.get('PASSWORD')

random=Random()

structure={}
structure["username"]=username
structure["password"]=password
structure["apiKey"]=apiKey
structure["defs"]={}
structure["nulls"]=[]

picklefile = "expand-filter.pickle"
if(os.path.isfile(picklefile)):
	structure=pickle.load(open(picklefile, "r"))

client = swagger.ApiClient(structure["apiKey"], apiUrl)
wordApi = WordApi.WordApi(client)

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

steps=0
for line in sys.stdin.readlines():
	nl=u''
	for word in line.split():
		word=unicode(word, 'utf8')
		steps=steps+1
		if(steps>1000):
			pickle.dump(structure, open(picklefile, "w"))
			steps=0
		if(word in structure["nulls"]):
			nl=nl+u' '+word
		elif(word in structure["defs"]):
			try:
				nl=nl+u' '+random.choice(structure["defs"][word])
			except:
				nl=nl+u' '+word
		else:
			try:
				defn=wordApi.getDefinitions(word, sourceDictionaries="all")
				if(defn==None or len(defn)==0):
					nl=nl+u' '+word
					structure["nulls"].append(word)
				else:
					l=[]
					for d in defn:
						l.append(d.text)
					structure["defs"][word]=l
					nl=nl+u' '+random.choice(l)
			except:
				nl=nl+u' '+word
				structure["nulls"].append(word)
	nl.strip()
	print(nl)
	sys.stdout.flush()
pickle.dump(structure, open(picklefile, "w"))

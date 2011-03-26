# Pyhton  :: 
# ZAP text 
# a script to make a one month dump of different RSS feed 
# by A Mazieres 
# and S Huron

# txml


import csv
import urllib
import feedparser
import string
import os.path
from datetime import datetime

MyRssTarget = csv.reader(open("MyRssTarget.csv","rb"))#, delimiter=':'
MyLastLoadF = open("MyLastLoad.csv", "r")
MyLastLoad  = csv.reader(MyLastLoadF)
MyOldUrl    = MyLastLoadF.read() 

def CheckMyURL(MyURL):
	MyCheck = 1;
	for row in MyLastLoad:
		if(row[0]==MyURL):
			MyCheck = 0
	return MyCheck

def NameSimple(name):
	name = name.strip()
	name = name.replace('\t','')
	nameT = name.split('/')
	SimpleName = nameT[len(nameT)-2]+nameT[len(nameT)-1]
	return SimpleName


#lire chaque ligne du CSV MyRssTarget
for row in MyRssTarget:
	print row[1]+'|'+row[2]
	page = urllib.urlopen(row[2])
	strpage = page.read()
	#print strpage	
	
	filename = "_"+row[0]+"-"+row[1]+".xml"
	filename = filename.strip()
	filename = filename.replace('\t','')
	print filename
	fichier = open(filename, "w")
	fichier.write(strpage)
	fichier.close()
	
	d = feedparser.parse(strpage)
	dLen = len(d['entries'])
	
	if (dLen!=0):
		for roww in d.entries:
			# print " -> "+roww.title.encode("utf-8")
			# print " -> "+roww.link.encode("utf-8")
			# Utiliser l'URL comme ID 
			# si elle existe pas je l'enregistre dans mon CSV et le fichier pointer dans un rep 
			MyUrlToLoad = roww.link.encode("utf-8")
			MyTest = CheckMyURL(MyUrlToLoad)
			print MyTest
			if(MyTest==1):
				
				MyHtmlpageFileName = NameSimple(MyUrlToLoad)
				print MyHtmlpageFileName
				# garder l'url pour l'enregistrer dans le CSV
				MyOldUrl += ",\n"+MyUrlToLoad#+" , "+MyHtmlpageFileName
				# sauver la page
				MyHtmlpage 		   = urllib.urlopen(MyUrlToLoad)
				MyStrHtmlpage 	   = MyHtmlpage.read()
				MyHtml = open(MyHtmlpageFileName, "w")
				MyHtml.write(MyStrHtmlpage)
				MyHtml.close()
				print MyHtmlpageFileName;
	else:
		print " merde !"
		
	print len(d['entries'])


fichier = open("MyLastLoad.csv", "w")
fichier.write(MyOldUrl)
fichier.close()

#def NameSimplify(name):
#def RepSimplify(name):
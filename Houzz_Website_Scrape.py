#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import urllib2
from bs4 import BeautifulSoup
import csv 
import sys
import time
import random


# Takes one argument:
# 1. City and State in the "[city]--[State Initial]" format
# 2. The amount of records available in a specific search


def WriteDictToCSV(csv_columns,dict_data):
	with open("houzz.csv", 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		#writer.writeheader()
		for row in dict_data:
			print row
			writer.writerow(row)

csv_columns =[ 'Name', 'Website']


for k in range(0, int(sys.argv[2]), 15):

	r = urllib2.urlopen("http://www.houzz.com/professionals/kitchen-and-bath/c/%s/d/100/p/%s" %(sys.argv[1], k))
	print k

	bs = BeautifulSoup(r, "lxml")
	url = bs.find_all("a", class_="pro-title")
	data =[]
	for u in url:
		output = {}
		link = u["href"]
		if link != "javascript:;":
			try:
				s = urllib2.urlopen(link)
			except:
				continue

			su = BeautifulSoup(s, "lxml")
			name = su.find("a", class_="profile-full-name")
			if name is not None:
				n = name.text.encode("utf-8")
				output["Name"] = n

			web = su.find("a", class_="proWebsiteLink")
			if web is not None:
				website = web["href"]
				output["Website"] = website

			data.append(output)

			print output

			time.sleep(random.randint(6, 11))

	#Writes to "houzz.csv every 15 successful entries"
	WriteDictToCSV(csv_columns,data)











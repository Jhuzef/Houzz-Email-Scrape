#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import csv
import time
import random
from webscraping import download
import Tkinter
import sys

def write(string):
    text_box.config(state=Tkinter.NORMAL)
    text_box.insert("end", str(string) + "\n")
    text_box.see("end")
    text_box.config(state=Tkinter.DISABLED)

def run(initials, city):
	reload(sys)
	sys.setdefaultencoding('utf-8')

	header = str(city) + "--" + str(initials)
	main(header)




def WriteDictToCSV(csv_columns,dict_data):
	with open("houzz.csv", 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		for row in dict_data:
			print row
			writer.writerow(row)


def EmailScrape(email):
	D = download.Download()
	emails = D.get_emails("{}".format(email), max_depth=1, max_urls=None, max_emails=25)
	return emails


def main(header):
	csv_columns = ['Name', 'Website', 'Email 1', 'Email 2', 'Email 3', 'Email 4', 'Email 5',
				   'Email 6', 'Email 7', 'Email 8', 'Email 9', 'Email 10', 'Email 11', 'Email 12', 'Email 13',
				   'Email 14', 'Email 15', 'Email 16', 'Email 17', 'Email 18', 'Email 19', 'Email 20', 'Email 21',
				   'Email 22', 'Email 23', 'Email 24', 'Email 25']

	for k in range(0, 100000, 5):

		r = urllib2.urlopen("http://www.houzz.com/professionals/kitchen-and-bath/c/%s/d/100/p/%s" %(header, k))
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
					emails = EmailScrape(website)
					for x in range(0, len(emails)):
						output["Email {}".format(x+1)] = emails[x]
				data.append(output)

				print output

				time.sleep(random.randint(6, 11))

		#Writes to "houzz.csv every 15 successful entries"
		WriteDictToCSV(csv_columns,data)

root = Tkinter.Tk()


Tkinter.Label(root, text="Initials of the State").grid(row=1)
Tkinter.Label(root, text="City Name").grid(row=2)

initials = Tkinter.Entry(root)
city = Tkinter.Entry(root)

initials.grid(row=1, column=1)
city.grid(row=2, column=1)


button_1 = Tkinter.Button(root, text="Enter", command=lambda: run(initials.get(), city.get()))
button_1.grid(row=3, column=0)


root.mainloop()
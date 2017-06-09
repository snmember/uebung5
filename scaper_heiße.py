from bs4 import BeautifulSoup
import requests
import csv
import os

def getPage(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    return soup
topthreewords = open ('top3words.csv','w')
csvword = csv.writer(topthreewords, delimiter = ';')




def main():
	heise_header = open('heise_header.csv', 'w')      # open file
	csvw = csv.writer(heise_header, delimiter = ';') 
	
	for j in range (0,4,1):
		soup = getPage("https://heise.de/thema/https?seite="+str(j)+" ")	
		soup_header = soup.find_all("header")
		for i in range (2,32,1):
			headerstring = soup_header[i].string
			if (headerstring != None):
				headerstring = headerstring.replace('\n','')
				headerstring = headerstring.replace('\r','')
				csvw.writerow([headerstring])
				headerstring = headerstring.replace('(','')
				headerstring = headerstring.replace(')',' ')
				headerstring = headerstring.replace('[','')
				headerstring = headerstring.replace(']',' ')
				headerstring = headerstring.replace(',','')
				headerstring = headerstring.replace(':','')
				headerstring = headerstring.replace('"','')
				headerstring = headerstring.replace('-',' ')
				words(headerstring,0)
				#headerstring = headerstring.encode("utf-8")
				
	topthreewords.close()
	wordlist = []
	reader = csv.reader(open("top3words.csv"))
	for row in reader:
		if (row != []):
			wordlist.append(row[0])
	first =("",0)
	second =("",0)
	third =("",0)
	for o in range (0,(len(wordlist)-1),1):
		if (wordlist[o]!= first[0] and wordlist[o]!= second[0] and wordlist[o]!= third[0]):
			word_count = wordlist.count(wordlist[o])
			if (word_count>first[1]):
					third = second
					second = first
					first = (str(wordlist[o]), word_count)
			else:
				if(word_count>second[1]):
					third = second
					second = (str(wordlist[o]),word_count)	
				else:
					if(word_count>third[1]):
						third = (str(wordlist[o]), word_count)
		
	print ("3 most used words in header")
	print (first)
	print (second)
	print (third)
	os.remove("top3words.csv")
 
						
def words(text,pos):
	
	#new_pos = text.find(" ",pos)
	ending_space= text.find(" ",pos)
	if (ending_space == -1):
		ending = len(text) + 1
		temp_name= text[pos:ending]
		csvword.writerow([temp_name])
	else:

		temp_name= text[pos:ending_space]
		csvword.writerow([temp_name])
		#word.append(temp_name)
		words(text,ending_space+1)

if __name__ == '__main__':
	main()

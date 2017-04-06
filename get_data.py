#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re


def parser_txt_to_data(filepath):
	#use beautifulsoup and re convert xml to no-clean data list
	soup = BeautifulSoup(open(filepath),"lxml")
	list_summary = soup.find_all("summary")
	list_short_text = soup.find_all("short_text")
	list_summary = [re.sub("<.*>","",str(summary)).strip() for summary in list_summary]
	list_short_text = [re.sub("<.*>","",str(short_text)).strip() for short_text in list_short_text]
	return list_summary , list_short_text

def clean_data(filepath):
	# use re to delete useless information in data
	list_summary , list_short_text = parser_txt_to_data(filepath)

	def _remove_special_char(m):
		s = m.group(0)
		if s in u'，。！？；“”：《》':
			return s
		return ''

	for i,line in enumerate(list_summary):
		line = line.decode('utf-8')
		line = re.sub(u'[\(\[（#「【\)\]）#」】]', '', line)
		list_summary[i] = re.sub(u'[^\u4e00-\u9fa50-9a-zA-Z]', _remove_special_char, line).encode('utf-8')
	
	for i,line in enumerate(list_short_text):
		line = line.decode('utf-8')
		line = re.sub(u'[\(\[（#「【\)\]）#」】]', '', line)
		list_short_text[i] = re.sub(u'[^\u4e00-\u9fa50-9a-zA-Z]', _remove_special_char, line).encode('utf-8')

	'''
	for i,line in enumerate(list_summary):
		print i;
		print list_summary[i]
		print list_short_text[i]
	'''
	return list_summary , list_short_text



if __name__ == "__main__":
	filepath = "./LCSTS/DATA/PART_II.txt"
	clean_data(filepath)

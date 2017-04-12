#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import codecs
import thulac
import sys

def iter_xml(filepath):
	f = open(filepath,'r')
	xml_text = []
	for line in f:
		line = line.rstrip()
		line = re.sub('<BR/>',"",line)
		line = re.sub('<BR>',"",line)
		line = re.sub('<br>',"",line)
		xml_text.append(line)
		if re.match('</doc>',line):
			yield '\n'.join(xml_text)
			xml_text = []
	f.close()
	

def parser_txt_to_data(filepath):
	#use beautifulsoup and re convert xml to no-clean data list
	list_summary = []
	list_short_text = []
	wrong_number = 0
	for i,xml_text in enumerate(iter_xml(filepath)):
		soup = BeautifulSoup(xml_text,"lxml")
		summary_soup = soup.find("summary")
		short_text_soup = soup.find("short_text")
		#if i%10000 == 0:
		#	print "parser %d"%(i)
		try:
			summary = summary_soup.string.strip()
			short_text = short_text_soup.string.strip()
			list_summary.append(summary)
			list_short_text.append(short_text)
		except:
			wrong_number+=1
			print ("wrong_number is %d"%(wrong_number))

	#print len(list_summary),type(list_summary),type(list_summary[0]),len(list_short_text),type(list_short_text),type(list_short_text[0]),list_summary[0]
	return list_summary , list_short_text

def get_clean_data(filepath):
	# use re to delete useless information in data
	list_summary , list_short_text = parser_txt_to_data(filepath)

	def _remove_special_char(m):
		s = m.group(0)
		if s in u'，。！？；“”：《》':
			return s
		return ''

	for i,line in enumerate(list_summary):
		line = re.sub(u'[\(\[（#「【\)\]）#」】]', '', line)
		list_summary[i] = re.sub(u'[^\u4e00-\u9fa50-9a-zA-Z]', _remove_special_char, line).encode('utf-8')
	
	for i,line in enumerate(list_short_text):
		line = re.sub(u'[\(\[（#「【\)\]）#」】]', '', line)
		list_short_text[i] = re.sub(u'[^\u4e00-\u9fa50-9a-zA-Z]', _remove_special_char, line).encode('utf-8')
	
	#print len(list_summary),type(list_summary),len(list_short_text),type(list_short_text)
	return list_summary , list_short_text

def get_partIII_label():
	#return partIII's label
	soup = BeautifulSoup(open("./LCSTS/DATA/PART_III.txt"),"lxml")
	list_label = soup.find_all("human_label")
	list_label = [re.sub('[^1-5]','',str(label)).strip() for label in list_label]
	return list_label

def return_cut_word_list_list(filepath):
	#return summary and short text[[],[],[]]
	list_summary , list_short_text = get_clean_data(filepath)
	thu_cut = thulac.thulac("-seg_only")
	list_word_short_text = []
	list_word_summary = []
	for i,short_text in enumerate(list_short_text):
		list_temp = thu_cut.cut(short_text)
		#if i%10000 == 0:
		#	print i," ".join(list_temp)
		list_word_short_text.append(list_temp)
	for i,summary in enumerate(list_summary):
		# list_temp = list(" ".join(thu_cut.cut(summary)))
		list_temp = thu_cut.cut(summary)
		#if i%10000 == 0:
		#	print i," ".join(list_temp)
		list_word_summary.append(list_temp)
	
	#print len(list_word_summary[0]), ' '.join(list_word_summary[0])
	return list_word_summary , list_word_short_text

def write_cut_word_to_file():
	#write summary and short text to file
	filepath = "./LCSTS/DATA/PART_I.txt"
	list_summary , list_short_text = get_clean_data(filepath)
	thu_cut = thulac.thulac("-seg_only")
	
	f_short_text = open("./LCSTS/DATA/PART_I_cut_short_text.txt","w+")
	f_summary = open("./LCSTS/DATA/PART_I_cut_summary.txt","w+")

	print len(list_summary),type(list_summary),len(list_short_text),type(list_short_text)
	for i,short_text in enumerate(list_short_text):
		list_temp = thu_cut.cut(short_text)
		try:
			content = " ".join(list_temp)
			#if i%5000 == 0:
			#	print i,content
		except:
			content = "wrong short text"
		f_short_text.write(content+"\n")
	
	f_short_text.close()

	for i,summary in enumerate(list_summary):
		list_temp = thu_cut.cut(summary)
		try:
			content = " ".join(list_temp)
			#if i%5000 == 0:
			#	print i,content
		except:
			content = "wrong summary"
		f_summary.write(content+"\n")
		
	f_summary.close()

def get_cut_PARTI_short_text():
	f = open("./LCSTS/DATA/PART_I_cut_short_text.txt",'r')
	list_cut_short_text = []
	for i,line in enumerate(f):
		#if i%10000==0:
		#	print i,line
		temp_list = line.split(' ')
		list_cut_short_text.append(temp_list)
	print len(list_cut_short_text),type(list_cut_short_text),type(list_cut_short_text[0])
	return list_cut_short_text


if __name__ == "__main__":
	filepath = "./LCSTS/DATA/PART_III.txt"
	#get_cut_PARTI_short_text()
	_,list_word_short_text = return_cut_word_list_list(filepath)
	print len(list_word_short_text),type(list_word_short_text),list_word_short_text[0]

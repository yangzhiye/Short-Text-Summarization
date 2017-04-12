#-*- coding: utf-8 -*-
from gensim import models,corpora
import get_data
import re

def cal_tfidf(filepath):
	_,list_word_short_text = get_data.return_cut_word_list_list(filepath)
	#print len(list_word_short_text),type(list_word_short_text),len(list_word_short_text[0]),type(list_word_short_text[0])
	dic = corpora.Dictionary.load("./model/dictionary.tfidf.dic")
	model_tfidf = models.TfidfModel.load("./model/PARTI_tfidf_model")
	corpus = [dic.doc2bow(text) for text in list_word_short_text]
	#print " ".join(list_word_short_text[0])
	for i,text in enumerate(corpus):
		for j,line in enumerate(model_tfidf[text]):
			if line[-1]>0.2 and line[0]!=999 and not re.match("^[0-9]*$",dic.get(line[0])):
				print dic.get(line[0]) 
	#print corpus_tfidf


if __name__ == "__main__":
	filepath = "./LCSTS/DATA/PART_III.txt"
	cal_tfidf(filepath)

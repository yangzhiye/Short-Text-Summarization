# -*- coding: utf-8 -*-
import sys
import get_data
import thulac
import logging

from gensim import models , corpora


def train_TFIDF():
	
	list_cut_short_text = get_data.get_cut_PARTI_short_text()
	
	print "list_cut_short_text is %d"%(len(list_cut_short_text))

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level = logging.INFO)
	
	dictionary = corpora.Dictionary(list_cut_short_text)

	dictionary.save("dictionary.tfidf.dic")
	
	corpus = [dictionary.doc2bow(text) for text in list_cut_short_text]

	tfidf = models.TfidfModel(corpus)
	
	tfidf.save('./model/PARTI_tfidf_model')


if __name__ == "__main__":
	
	train_TFIDF()

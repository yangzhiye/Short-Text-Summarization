#-*- coding: utf-8 -*-
from gensim import models,corpora
import get_data
import re
import heapq

def get_max_k_tuple_list(tuple_list,k):
	# use heap to return max k tuple
	return heapq.nlargest(k,tuple_list,key = lambda x:x[1])

def get_index_of_summary(dic,model_tfidf,corpus_list,k,list_word):
	wrong_word_list = [u'；',u'而']
	#print " ".join(list_word)
	corpus_list = [word_tuple for word_tuple in corpus_list \
		if dic.get(word_tuple[0]) not in wrong_word_list and not re.match("^\d*$", dic.get(word_tuple[0]))]
	
	list_max_k = get_max_k_tuple_list(model_tfidf[corpus_list],k)
	list_max_word = [dic.get(t[0]) for t in list_max_k]
	#print " ".join(list_max_word) 
	cal_list = []
	s = " ".join(list_word)
	ans_value = 0.0
	ans = ""
	#re.split('，|。|；|？|！',"".join(list_word))[i]
	for i,sen in enumerate(re.split('，|。|；|？|！',s)):
		sen_list = sen.split(' ')	
		temp_list = []
		temp_value = 0.0
		n = 0
		#print sen_list
		#print i,sen,len(sen)
		for j,word in enumerate(sen_list):
			if word.decode("utf8") in list_max_word:
				temp_list.insert(j,1)
			else:
				temp_list.insert(j,0)
		#print i,temp_list
		length = 0
		for k in temp_list:
			length += 1
			if k==1:
				n += 1
		try:
			temp_value = n*n*1.0/length
		except:
			temp_value = 0
		#print i,n,length,temp_value
		if length>=5 and length<=15 and temp_value > ans_value:
			ans_value = temp_value
			ans = re.split('，|。|；|？|！',"".join(list_word))[i]
	
	return ans

def use_tfidf_cal_summary(filepath):
	_,list_word_short_text = get_data.return_cut_word_list_list(filepath)
	dic = corpora.Dictionary.load("./model/dictionary.tfidf.dic")
	model_tfidf = models.TfidfModel.load("./model/PARTI_tfidf_model")
	corpus = [dic.doc2bow(text) for text in list_word_short_text]
	
	for i,tuple_list in enumerate(corpus):
		#if i>0:
		#	break
		ans = get_index_of_summary(dic,model_tfidf,tuple_list,10,list_word_short_text[i])
		print ans
	

'''
def test_a_cal_tfidf(filepath):
	_,list_word_short_text = get_data.return_cut_word_list_list(filepath)
	
	dic = corpora.Dictionary.load("./model/dictionary.tfidf.dic")
	model_tfidf = models.TfidfModel.load("./model/PARTI_tfidf_model")
	corpus = [dic.doc2bow(text) for text in list_word_short_text]
	
	print len(list_word_short_text[0])
	s = "".join(list_word_short_text[0])
	print s
	s2 = " ".join(list_word_short_text[0])
	print s2
	#for i,sen in enumerate(re.split('；|。',s)):
	#	print sen
	print corpus[0]
	for i,t in enumerate(corpus[0]):
		#  remove ;
		if t[0] == 999 or dic.get(t[0])=="而".decode("utf8"):
			corpus[0].remove(corpus[0][i])
	list_max_k = get_max_k_tuple_list(model_tfidf[corpus[0]],10)
	list_max_word = [dic.get(t[0]) for t in list_max_k]
	print " ".join(list_max_word)
	cal_list = []
	for i,word in enumerate(list_word_short_text[0]):
		if word.decode("utf8") in list_max_word:
			cal_list.insert(i,1)
		else:
			cal_list.insert(i,0)
	print cal_list	
	ans = 0
	n = 0
	cur = 0
	left = 0
	right = 0
	index_list = []
	cur = 0
	threshold_of_word = 5
	cur_threshold = 0
	flag = 0
	for i,index in enumerate(cal_list):
		if index == 1:
			index_list.append(i)
	print index_list
	for i,first in enumerate(index_list):
		for j,second in enumerate(index_list):
			if second - first >=5 and second -first <= 15:
				for k in range(first,second+1):
					if cal_list[k] == 0:
						cur_threshold+=1
						if cur_threshold>=threshold_of_word:
							flag = 1
							cur_threshold = 0
							break
					if cal_list[k] == 1:
						n+=1
						cur_threshold = 0
				if flag==1:
					flag=0
					break;
				cur = n*n*1.0/(second+1-first)
				n = 0
				if cur>ans:
					left = first
					right = second
					ans = cur
	ans_list = list_word_short_text[0][left:right+1]
	print "".join(ans_list)
'''

if __name__ == "__main__":
	filepath = "./LCSTS/DATA/PART_III.txt"
	#cal_tfidf(filepath)
	use_tfidf_cal_summary(filepath)

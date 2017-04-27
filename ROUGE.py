#-*- coding: utf-8 -*-

def ROUGE1_character_based(list_predict,list_true):
	match_gram = 0
	all_gram = 0
	for i,s_predict in enumerate(list_predict):
		s_predict = s_predict.decode("utf8")
		s_true = list_true[i].decode("utf8")
		for j,word in enumerate(s_predict):
			if word in s_true:
				match_gram+=1
		all_gram += len(s_true)
	#print "match_gram is:",match_gram
	#print "all_gram is:",all_gram

	return match_gram*1.0/all_gram
	

def ROUGE2_character_based(list_predict,list_true):
	match_gram = 0
	all_gram = 0
	for i,s_predict in enumerate(list_predict):
		s_predict = s_predict.decode("utf8")
		s_true = list_true[i].decode("utf8")
		for j,word in enumerate(s_predict):
			if j > 0:
				for k,true_word in enumerate(s_true):
					if k > 0:
						if word==true_word and s_predict[j-1] == s_true[k-1]:
							match_gram+=1
							break
		all_gram += len(s_true)-1
	#print "match_gram is:",match_gram
	#print "all_gram is:",all_gram
	
	return match_gram*1.0/all_gram


def ROUGE_SU4(list_predict,list_true,beta):
	match_gram = 0
	all_gram = 0
	for i,s_predict in enumerate(list_predict):
		s_predict = s_predict.decode("utf8")
		s_true = list_true[i].decode("utf8")
		for j,word in enumerate(s_predict):
			if word in s_true:
				match_gram+=1
		all_gram += len(s_true)
	
	for i,s_predict in enumerate(list_predict):
		s_predict = s_predict.decode("utf8")
		s_true = list_true[i].decode("utf8")
		for j,word in enumerate(s_predict):
			for k in range(1,6):
				flag = 0
				if j+k<len(s_predict):
					for m,true_word in enumerate(s_true):
						if flag == 1:
							break
						for n in range(1,6):
							if m+n < len(s_true):
								if word==true_word and s_predict[j+k] == s_true[m+n]:
									match_gram += 1
									flag = 1
									break

	predict_all_gram = 0
	true_all_gram = 0

	for i,s_predict in enumerate(list_predict):
		s_predict = s_predict.decode("utf8")
		s_true = list_true[i].decode("utf8")
		predict_all_gram+=((len(s_predict)-5)*5+9)
		true_all_gram+=((len(s_true)-5)*5+9)

	predict_all_gram+=all_gram
	true_all_gram+=all_gram
	R = match_gram*1.0/true_all_gram
	P = match_gram*1.0/predict_all_gram
	F = (1+beta*beta)*1.0*P*R/(R+(beta*beta*P))
	print "R is:",R
	#print "P is:",P
	print "F is:",F
	return R,P,F



if __name__ == "__main__":
	list_predict = ["我是正确的摘要其他的都是假的","杨志烨无敌"]
	list_true = ["我是不对的摘要哈哈哈假的","基本无敌吧"]
	print ROUGE1_character_based(list_predict,list_true)
	print ROUGE2_character_based(list_predict,list_true)
	ROUGE_SU4(list_predict,list_true,1)

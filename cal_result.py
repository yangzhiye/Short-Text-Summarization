import get_data
import ROUGE


def cal_ROUGE(result_filepath):
	
	list_true_summary, _ = get_data.parser_txt_to_data("./LCSTS/DATA/PART_III.txt")
	f = open(result_filepath)
	list_predict_summary = []
	for i , line in enumerate(f.readlines()):
		list_predict_summary.append(line)
	list_true_summary = [summary.encode("utf8") for summary in list_true_summary]

	print ROUGE.ROUGE1_character_based(list_predict_summary,list_true_summary)
	print ROUGE.ROUGE2_character_based(list_predict_summary,list_true_summary)
	ROUGE.ROUGE_SU4(list_predict_summary,list_true_summary,1)



if __name__ == "__main__":
	for k in range(5,16):
		print "k is %d"%(k)
		cal_ROUGE("./result/EK_tfidf_result/0426_k=%d.txt"%(k))


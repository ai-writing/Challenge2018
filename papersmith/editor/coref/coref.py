# -*- coding: UTF-8 -*-

from neuralcoref import Coref
import os
import json
import sys, getopt

# pronoun = ["I", "me", "my", "mine", "myself", "you", "your", "yours", "yourself", "he", "him", "his", "himself",
#            "she", "her", "hers", "herself", "it", "its", "itself", "we", "us", "our", "ours", "ourselves", "yourselves",
#            "they", "them", "their", "theirs", "themselves"]


def coref(content):
	import re
	coref = Coref()
	clusters = coref.continuous_coref(
		utterances=content)
	clu = coref.get_clusters(remove_singletons=False)
	for i in clu:
		print(clu[i])

	result = []
	mentions = coref.get_mentions()
	utterances = coref.get_utterances()
	print(utterances)
	indexs = [(1, 0)]
	for men in mentions:
		ment = re.compile('\W' + str(men) + '\W')
		search = re.search(ment, content[indexs[men.index][0] - 1:])
		tempindex = indexs[men.index][0] - 1
		temptuple = (search.start() + 1 + tempindex, search.end() - 1 + tempindex)
		if temptuple == indexs[men.index]:
			search = re.search(ment, content[indexs[men.index][1]:])
			tempindex = indexs[men.index][1]
			temptuple = (search.start() + 1 + tempindex, search.end() - 1 + tempindex)
		indexs.append(temptuple)
		if men.mention_type == 0:
			isre = False
			for i in clu:
				if men.index in clu[i]:
					isre = True
					break
			if not isre:
				result.append([temptuple])

		print(men.index, men, indexs[men.index + 1], men.mention_type)

	score = coref.get_scores()
	for id in score['single_scores']:
		print(id, score['single_scores'][id])
		if mentions[id].mention_type == 0:
			if score['single_scores'][id] > 0.2:
				if str(mentions[id]) != 'It' and str(mentions[id]) != 'it':
					result.append([indexs[id + 1]])
	# for id in score['pair_scores']:
	for id in score['pair_scores']:
		first = (0, 0)
		second = (0, 0)
		for pair in score['pair_scores'][id]:
			pairvalue = score['pair_scores'][id][pair]
			if pairvalue > first[1]:
				first = (pair, pairvalue)
			elif pairvalue > second[1]:
				second = (pair, pairvalue)
		if first[1] > 0 and second[1] > 0 and first[1] - second[1] < 2.8:
			print(first[1],second[1])
			result.append([indexs[id + 1], indexs[first[0] + 1], indexs[second[0] + 1]])
		print(id, score['pair_scores'][id])
	print(result)
	return result


if __name__ == "__main__":
	coref(
		"I like Bill and Jack. He is very tall. He is handsome. He killed Jack, the younger child, who is a singer. What is that? It is her friend who loves a dog. Its name is Mike.")

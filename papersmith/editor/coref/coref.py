# -*- coding: UTF-8 -*-

from neuralcoref import Coref
import os
import json
import sys, getopt
from papersmith.editor.issue import Issue

# pronoun = ["I", "me", "my", "mine", "myself", "you", "your", "yours", "yourself", "he", "him", "his", "himself",
#            "she", "her", "hers", "herself", "it", "its", "itself", "we", "us", "our", "ours", "ourselves", "yourselves",
#            "they", "them", "their", "theirs", "themselves"]


def coref(_content):
	import re
	coref = Coref()
	content=_content.replace("\n",'')
	clusters = coref.continuous_coref(
		utterances=content)
	clu = coref.get_clusters(remove_singletons=False)
	utterances=coref.get_utterances()
	print(utterances)
	result = []
	mentions = coref.get_mentions()
	utterances = coref.get_utterances()
	# print("***************88")
	# print(utterances)
	# print(mentions)
	if len(mentions) <= 1:
		return []
	indexs = [(0, 0)]
	for men in mentions:
		strmen = str(men)
		if strmen[-1] in ['.', '?', '!', ',']:
			strmen = strmen[:-1]
		ment = re.compile('\\b' + strmen + '\\b')
		search = re.search(ment, content[indexs[men.index][0]:])
		if not search:
			indexs.append(indexs[men.index])
			continue
		tempindex = indexs[men.index][0]
		temptuple = (search.start() + tempindex, search.end() + tempindex)
		if temptuple == indexs[men.index]:
			search = re.search(ment, content[indexs[men.index][1]:])
			tempindex = indexs[men.index][1]
			temptuple = (search.start() + tempindex, search.end() + tempindex)
		indexs.append(temptuple)
		if men.mention_type == 0:
			isre = False
			for i in clu:
				if men.index in clu[i]:
					isre = True
					break
			if not isre:
				result.append([temptuple])

		# print(men.index, men, indexs[men.index + 1], men.mention_type)

	score = coref.get_scores()
	for id in score['single_scores']:
		# print(id, score['single_scores'][id])
		if mentions[id].mention_type == 0:
			if score['single_scores'][id] and score['single_scores'][id] > 0.2:
				if str(mentions[id]) != 'It' and str(mentions[id]) != 'it':
					result.append([indexs[id + 1]])

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
			# print(id, first[1],second[1])
			result.append([indexs[id + 1], indexs[first[0] + 1], indexs[second[0] + 1]])
		if mentions[id].mention_type==0 and first[1] < 2:
			if str(mentions[id]) != 'It' and str(mentions[id]) != 'it':
				result.append([indexs[id + 1]])
		# print(id, score['pair_scores'][id])

	results = []
	for id in result:
		if id not in results:
			results.append(id)
	print(results)


	startlist = []
	endlist = []
	issues = []
	for lists in results:
		for cor in lists:
			startlist.append(cor[0])
			endlist.append(cor[1])
		issue = Issue(1, 1, startlist, endlist, 'wrong', 0)
		issues.append(issue)
		startlist = []
		endlist = []
	return issues


if __name__ == "__main__":
	coref(
		"I like Bill and Jack. He is very tall.\n")

# They like Bill and Jack. He is very tall. He is handsome. He saw Jack, the younger child, who is a singer. What is that? It is her friend who loves a dog. Its name is Mike.

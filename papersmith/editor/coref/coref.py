# -*- coding: UTF-8 -*-

from neuralcoref import Coref
import os
import json
import sys, getopt
import spacy

from papersmith.editor.issue import Issue

pronoun = ["I", "me", "my", "mine", "myself", "you", "your", "yours", "yourself", "we", "us", "our", "ours",
           "ourselves", "yourselves",
           "I", "Me", "My", "Mine", "Myself", "You", "Your", "Yours", "Yourself", "We", "Us", "Our", "Ours",
           "Ourselves", "Yourselves",
           ]

notpro = []

print("Loading spacy model")
try:
	spacy.info('en_core_web_sm')
	model = 'en_core_web_sm'
except IOError:
	print("No spacy 2 model detected, using spacy1 'en' model")
	model = 'en'
nlp = spacy.load(model)

def coref(_content):
	import re

	coref = Coref(nlp)
	content = _content.replace("\n", '')
	clusters = coref.continuous_coref(
		utterances=content)
	clu = coref.get_clusters(remove_singletons=False)
	utterances = coref.get_utterances()
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
				if str(men) != 'It' and str(men) != 'it' and str(men) not in pronoun:
					result.append([temptuple])
				else:
					notpro.append(men.index)

		print(men.index, men, indexs[men.index + 1], men.mention_type)

	score = coref.get_scores()
	for id in score['single_scores']:
		print(id, score['single_scores'][id])
		if mentions[id].mention_type == 0:
			if score['single_scores'][id] and score['single_scores'][id] > -0.3:
				print(mentions[id])
				if str(mentions[id]) != 'It' and str(mentions[id]) != 'it' and str(mentions[id]) not in pronoun:
					if str(mentions[id]) in notpro:
						print(mentions[id])
						result.append([indexs[id + 1]])
				else:
					notpro.append(id)

	print(notpro, result)
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
			print(id, first[1], second[1])
			print(first[0], second[0])
			firstid = first[0]
			secondid = second[0]
			if firstid < secondid:
				tempid = firstid
				firstid = secondid
				secondid = tempid
			if score['pair_scores'][firstid][secondid] > 2 or firstid - secondid > 15 \
					or indexs[firstid + 1][1] == indexs[secondid + 1][1] or indexs[firstid + 1][0] == \
					indexs[secondid + 1][0] \
					or firstid in notpro or secondid in notpro:
				print('reject')
			else:
				result.append([indexs[id + 1], indexs[first[0] + 1], indexs[second[0] + 1]])
		if mentions[id].mention_type == 0 and first[1] < 2:
			if str(mentions[id]) != 'It' and str(mentions[id]) != 'it' and str(mentions[id]) not in pronoun:
				result.append([indexs[id + 1]])
		print(id, score['pair_scores'][id])

	print(coref.get_most_representative())
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
		issue = Issue(2, 2, startlist, endlist, 'ambiguous pronouns', 0)
		issues.append(issue)
		startlist = []
		endlist = []
	return issues


if __name__ == "__main__":
	coref(
		"They like Bill and Jack. He is very tall. He is handsome. He saw Jack, the younger child, who is a singer. What is that? It is her friend who loves a dog. Its name is Mike.")

# They like Bill and Jack. He is very tall. He is handsome. He saw Jack, the younger child, who is a singer. What is that? It is her friend who loves a dog. Its name is Mike.
# It became the statistician's calculator for the 1990s, allowing easy access to the computing power and graphical capabilities of modern workstations and personal computers. Various implementations have been available, currently S-PLUS, a commercial system from the Insightful Corporation1 in Seattle, and R,2 an Open Source system written by a team of volunteers. Both can be run on Windows and a range of UNIX / Linux operating systems: R also runs on Macintoshes. This is the fourth edition of a book which first appeared in 1994, and the S environment has grown rapidly since. This book concentrates on using the current systems to do statistics; there is a companion volume  which discusses programming in the S language in much greater depth. Some of the more specialized functionality of the S environment is covered in on-line complements, additional sections and chapters which are available on the World Wide Web. The datasets and S functions that we use are supplied with most S environments and are also available on-line. This is not a text in statistical theory, but does cover modern statistical methodology.
# No part of this book may be reproduced in any form by any electronic or mechanical means without permission in writing from the publisher. MIT Press books may be purchased at special quantity discounts for business or sales promotional use. This book was set in Sabon by SNP Best-set Typesetter Ltd., Hong Kong. Printed and bound in the United States of America. Library of Congress Cataloging-in-Publication Data Stahl, Gerry. Group cognition : computer support for collaborative knowledge building / Gerry Stahl. The MIT Press Acting with Technology series is concerned with the study of meaningful human activity as it is mediated by tools and technologies. The goal of the series is to publish the best new books--both research monographs and textbooks-- that contribute to an understanding of technology as a crucial facet of human activity enacted in rich social and physical contexts. The focus of the series is on tool-mediated processes of working, playing, and learning in and across a wide variety of social settings. The series explores developments in postcognitivist theory and practice from the fields of sociology, communication, education, organizational studies, science and technology studies, human-computer interaction studies, and computer-supported collaborative work. It aims to encompass theoretical frameworks developed through cultural-historical activity theory, actor-network theory, distributed cognition, ethnomethodology, and grounded theory. In Group Cognition: Computer Support for Building Collaborative Knowledge, Gerry Stahl challenges us with the provocative notion that \"small groups are the engines of knowledge building.\" He notes that research on learning has focused on either individual cognition or the larger community.

# -*- coding: utf-8 -*-

import nltk

def check(content):
	sentence_tag = nltk.pos_tag(nltk.word_tokenize(content))
	grammar = r'NP:}<PRP$>{'
	tree = nltk.RegexpParser(grammar).parse(sentence_tag)
	print(tree)

check("I with me dog went to I father theater.")

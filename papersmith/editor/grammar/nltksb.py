# -*- coding: utf-8 -*-

import nltk

def check(content):
	s= nltk.pos_tag(nltk.word_tokenize(content))
	for i in s:
		if i[1]=='NN':
			print(i[0],len(i[0]))

check("yesterday I went to the theater.")

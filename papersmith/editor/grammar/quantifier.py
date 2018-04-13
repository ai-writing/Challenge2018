# -*- coding: utf-8 -*-

import nltk

def check(content):
	cno=['many','few','a few','a number of','the number of','numbers of','a quantity of','quantities of','a good many','a great many','a large number of','a great number of','scores of','dozens of']
	uno=['much','little','a little','huge amounts of','a great amount of','a large amount of','a great deal of','a large deal of','a plenty of','a good supply of','a piece of','a bit of','an item of', 'an article of','a bottle of','a cup of','a drop of','a glass of']
	sentence_tag = nltk.pos_tag(nltk.word_tokenize(content))
	for i in sentence_tag:
		print(i[0])
check('Last week I went to the theater.')

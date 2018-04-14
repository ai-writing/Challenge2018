# -*- coding: utf-8 -*-

import nltk
from papersmith.editor.issue import Issue

def check(content):
	cno=['many','few','a few','a number of','the number of','numbers of','a quantity of','quantities of','a good many','a great many','a large number of','a great number of','scores of','dozens of']
	uno=['much','little','a little','huge amounts of','a great amount of','a large amount of','a great deal of','a large deal of','a plenty of','a good supply of','a piece of','a bit of','an item of', 'an article of','a bottle of','a cup of','a drop of','a glass of']
	uncountable_nouns=eval(open('papersmith/editor/grammar/uncountable_nouns.txt').read())
	issues=[]
	w=''
	for i in range(len(content)):
		if (ord(content[i])>64 and ord(content[i])<91) or (ord(content[i])>96 and ord(content[i])<123) or content[i]=="'":
			w+=content[i]
			if len(w)==1 and w=='\'':
				w=''
			continue
		if len(w)==0:
			continue
		if w=='many' or w=='few':
			pos=i
			sentence=''
			for j in range(1000):
				if i>=len(content) or content[i]=='.' or content[i]=='!' or content[i]=='?' or content[i]==',' or content[i]==':' or content[i]==';':
					t=nltk.word_tokenize(sentence)
					l=nltk.pos_tag(t)
					for j in l:
						if j[1]=='NN':
							if j[0] in uncountable_nouns:
								if w=='many':
									issues.append(Issue(2, 1, [pos-4], [pos], 'much', 0))
								else:
									issues.append(Issue(2, 1, [pos-3], [pos], 'little', 0))
					break
				sentence+=content[i]
				i+=1
		w=''
	return issues
            
            
                    
                
                

# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue
from papersmith.editor.coref.coref import coref


def check(content):
	'检查内容中的语法错误'

	# do something with the content, which is a string
	print("Loading spacy model")
	try:
		spacy.info('en_core_web_sm')
		model = 'en_core_web_sm'
	except IOError:
		print("No spacy 2 model detected, using spacy1 'en' model")
		model = 'en'
	nlp = spacy.load(model)
	issues = coref(content, nlp)
	# Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py

	return issues  # List of issues

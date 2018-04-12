# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue
from papersmith.editor.coref.coref import coref

def check(content):
	'检查内容中的语法错误'

	# do something with the content, which is a string
	issues = coref(content)
	# Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py

	return issues  # List of issues

# -*- coding: utf-8 -*-
 
from issue import Issue
import tense
 
 
#djl
def checkTense(content):
    suggests=tense.tensecheck(content)
    issuesOfArticle = []
    for i in suggests:
        issue = Issue(2, 2, [i[0]], [i[1]], i[2], i[3])
        print(i)
        issuesOfArticle.append(issue)
    return issuesOfArticle
    
 
 
def check(content,tensechecker):
    '检查内容中的语法错误'
 
    issues = []
    issues += tensechecker.checkTense(content)
    issues += tensechecker.checkTense(content)
    # Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py
 
    #issues = [issue]
    return issues # List of issues'''
 
 
'''def check(content):
    '样例：检查内容中的语法错误'
 
    # do something with the content, which is a string
 
    issue = Issue(1, 1, [15], [19], 'replacement', 3)
        # Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py
 
    issues = [issue]
 
    return issues # List of issues'''
 
 
tensechecker=tense.Tense()
print(check("The fox is big, grew bigger. The rat was small but runs quickly."),tensechecker)

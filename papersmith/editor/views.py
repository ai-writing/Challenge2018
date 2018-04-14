# -*- coding: utf-8 -*-
"""Editor section"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import login_required, login_user, logout_user

# from papersmith.extensions import login_manager
# from papersmith.public.forms import LoginForm
# from papersmith.user.forms import RegisterForm
# from papersmith.user.models import User
from papersmith.utils import flash_errors
from papersmith.extensions import csrf_protect
from flask import jsonify
import json

from . import issue

from papersmith.editor.grammar import quantifier
from papersmith.editor.grammar import grammar
from papersmith.editor.grammar import PersonalPronoun
from papersmith.editor.spelling import capital
from papersmith.editor.spelling import spelling
from papersmith.editor.spelling import capital
from papersmith.editor.spelling.correction import gen_trie

blueprint = Blueprint('editor', __name__, static_folder='../static', template_folder='../templates/editor')
gen_trie()

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@blueprint.route('/api/num', methods=['GET', 'POST'])
@csrf_protect.exempt
def check():
    # using csrf exempt for now; to add csrf, refer to: http://flask.pocoo.org/snippets/3/
    # <form method=post action=""><input name=_csrf_token type=hidden value="{{ csrf_token() }}"></form>

    content = json.loads(request.data.decode('utf8'))['paperBody']
    print(content)
    grammar_results = grammar.check(content)
    spelling_results = spelling.check(content)
    spelling_results += capital.check(content)
    grammar_results += PersonalPronoun.check(content)
    grammar_results += quantifier.check(content)

    spelling_issues = {'err':[], 'sug': []}
    grammar_issues = {'err':[], 'sug': []}
    semantic_issues = {'err':[], 'sug': []}
    structure_issues = {'err':[], 'sug': []}

    # the counter is for generating id for the front-end
    counter = 0

    for issue in grammar_results:
        counter += 1
        if issue.itype == 1:   grammar_issues['err'].append(issue.export(counter))
        elif issue.itype == 2: grammar_issues['sug'].append(issue.export(counter))

    for issue in spelling_results:
        counter += 1
        if issue.itype == 1:   spelling_issues['err'].append(issue.export(counter))
        elif issue.itype == 2: spelling_issues['sug'].append(issue.export(counter))

    total_issues = len(spelling_issues['err']) + len(grammar_issues['err']) \
        + len(semantic_issues['err']) + len(structure_issues['err']) \
        + len(spelling_issues['sug']) + len(grammar_issues['sug']) \
        + len(semantic_issues['sug']) + len(structure_issues['sug'])

    return jsonify({
        "success":1,
        "count":{
            "id": 1,
            "errorSpelling": len(spelling_issues['err']),
            "errorGrammar": len(grammar_issues['err']),
            "errorSemantic": len(semantic_issues['err']),
            "errorStructure": len(structure_issues['err']),
            "suggestSpelling": len(spelling_issues['sug']),
            "suggestGrammar": len(grammar_issues['sug']),
            "suggestSemantic": len(semantic_issues['sug']),
            "suggestStructure": len(structure_issues['sug']),
            "sumNum": total_issues
        },
        "spelling": spelling_issues,
        "grammar": grammar_issues,
        "semantic": semantic_issues,
        "structure": structure_issues
    })

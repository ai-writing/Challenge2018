# -*- coding: utf-8 -*-
"""Editor section"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import login_required, login_user, logout_user

# from papersmith.extensions import login_manager
# from papersmith.public.forms import LoginForm
# from papersmith.user.forms import RegisterForm
# from papersmith.user.models import User
from papersmith.utils import flash_errors
from flask import jsonify

from . import issue

from papersmith.editor.grammar import grammar

blueprint = Blueprint('editor', __name__, static_folder='../static', template_folder='../templates/editor')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@blueprint.route('/api/num/', methods=['GET', 'POST'])
def check():
    grammar_results = grammar.check(request.data)

    spelling_issues = {'err':[], 'sug': []}
    grammar_issues = {'err':[], 'sug': []}
    semantic_issues = {'err':[], 'sug': []}
    structure_issues = {'err':[], 'sug': []}

    for issue in grammar_results:
        if issue.itype == 1:   grammar_issues['err'].append(issue.export())
        elif issue.itype == 2: grammar_issues['sug'].append(issue.export())

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
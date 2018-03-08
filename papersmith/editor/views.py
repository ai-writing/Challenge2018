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

@blueprint.route('/check/', methods=['GET', 'POST'])
def check():
    grammar_issues = grammar.check(request.data)

    json_issues = []
    spelling_errors = 5
    grammar_errors = 0
    grammar_suggestions = 0
    semantic_errors = 2
    semantic_suggestions = 4
    structure_suggestions = 1

    for issue in grammar_issues:
        json_issues.append(issue.export())
        if issue.itype == 1:   grammar_errors += 1
        elif issue.itype == 2: grammar_suggestions += 1

    total_issues = spelling_errors + grammar_errors + grammar_suggestions \
        + semantic_errors + semantic_suggestions + structure_suggestions

    return jsonify({
        "success":1,
        "data":{
            "id": 1,
            "errorSpelling": spelling_errors,
            "errorGrammar": grammar_errors,
            "errorLexeme": semantic_errors,
            "suggestLexeme": semantic_suggestions,
            "suggestStructure": structure_suggestions,
            "sumNum": total_issues
        },
        "issues": json_issues
    })
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

from papersmith.editor.grammar import grammar

blueprint = Blueprint('editor', __name__, static_folder='../static', template_folder='../templates/editor')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@blueprint.route('/check/', methods=['GET', 'POST'])
def check():
    grammarPosL, grammarPosR = grammar.check(request.data)
    return jsonify({
        "success":1,
        "data":{
            "id": 1,
            "errorSpelling": 5,
            "errorGrammar":2,
            "errorLexeme":4,
            "suggestLexeme":5,
            "suggestStructure":2,
            "sumNum":17,
            "errorSpellingPosL":[1,11,111],
            "errorSpellingPosR":[4,14,114],
            "errorSpellingRight":["hahaha","ooo","lalala"],
            "errorGrammarPosL": grammarPosL,
            "errorGrammarPosR": grammarPosR
        }
    })
# -*- coding: utf-8 -*-
"""Editor section"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import login_required, login_user, logout_user

# from papersmith.extensions import login_manager
# from papersmith.public.forms import LoginForm
# from papersmith.user.forms import RegisterForm
# from papersmith.user.models import User
from papersmith.utils import flash_errors

blueprint = Blueprint('editor', __name__, static_folder='../static', template_folder='../templates/editor')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

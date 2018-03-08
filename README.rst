===============================
PaperSmith
===============================

A scholarly writing enhancement tool.


Prerequisites
-------------
======================  ======================
Package name            How to get it?
======================  ======================
Node.js (includes npm)  `Node.js website<https://nodejs.org/en/>`_
Python 3 (recommended)  `Python website<https://www.python.org/downloads/>`_
PostgreSQL              `PostgreSQL website<https://www.postgresql.org/download/>`_
======================  ======================

Quickstart
----------

First, set your app's secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export PAPERSMITH_SECRET='something-really-secret'

Then, clone and build the front end ::

    git clone https://github.com/ai-writing/Front-End
    cd Front-End
    npm run build
    cd ..

Afterwards, copy the front end distribution to the back end project ::

    git clone https://github.com/ai-writing/Challenge2018
    cp -r Front-End/dist/static Challenge2018/papersmith/static
    mkdir Challenge2018/papersmith/templates/editor
    cp Front-End/dist/index.html Challenge2018/papersmith/templates/editor

It is recommended that you use virtualenv_ to manage the python environment.

.. _virtualenv: http://pythonguidecn.readthedocs.io/zh/latest/dev/virtualenvs.html

If you choose to use virtualenv, create a new env and activate it ::

    cd Challenge2018
    virtualenv venv
    . venv/bin/activate

Finally, run the following commands to bootstrap your environment (make sure you are in the ``Challenge2018`` directory) :: 

    brew install postgresql # run this if you use macOS and brew; otherwise please refer to "Prerequisites"
    pip install -r requirements/dev.txt
    npm install
    flask db init
    flask db migrate
    flask db upgrade
    npm start  # run the webpack dev server and flask server using concurrently

You will see a pretty welcome screen.

In general, before running shell commands, set the ``FLASK_APP`` and
``FLASK_DEBUG`` environment variables ::

    export FLASK_APP=autoapp.py
    export FLASK_DEBUG=1

Troubleshoot: If there's an error while running npm, consider upgrading to the latest version.


Back end development
--------------------

和后段开发有关的资源都在 ``Challenge2018/papersmith/editor/`` 目录下。

后端的语法、语义、句式检查分别作为一个 python package，存放在上述文件夹中。以 ``grammar`` package 为例，其中包含 ``grammar.py`` module，实现一个 ``check(content)`` 函数，其中 content 是前端传来的用户文章。

文章例子： ::

    # TODO

对于每个发现的问题，封装成 ``Issue`` 格式 (``Challenge2018/papersmith/editor/issue.py``) ::

    category:       1语法/2语义/3句式
    itype:          issue 类型：1错误/2建议/3普通；
    start:          起始下标，列表
    end:            终止下标+1，列表
    replacement:    替换成的字符串
    exp_id:         解释的编号

注意 ``start`` 和 ``end`` 是 ``list`` 类型，即使分别只有一个下标。非常简单的使用样例请看 ``Challenge2018/papersmith/editor/grammar/grammar-example.py``。


Deployment
----------

To deploy::

    export FLASK_DEBUG=0
    npm run build   # build assets with webpack
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.


Asset Management
----------------

Files placed inside the ``assets`` directory and its subdirectories
(excluding ``js`` and ``css``) will be copied by webpack's
``file-loader`` into the ``static/build`` directory, with hashes of
their contents appended to their names.  For instance, if you have the
file ``assets/img/favicon.ico``, this will get copied into something
like
``static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico``.
You can then put this line into your header::

    <link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">

to refer to it inside your HTML page.  If all of your static files are
managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in your ``settings.py``::

    SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year

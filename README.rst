ELTS
=====

This repo contains the source code for the Electronic Lending Tracking System
(ELTS). You can get the full source code for ELTS from
https://github.com/Ichimonji10/elts.git. ELTS is written using the Django web
app framework. For more on Django, read the excellent `Django documentation`_.

This document contains commands that should be run from a shell (command line).
Your shell's current working directory should be the root directory of this
repository. That is, you should ``cd`` to the directory containing this
document.

.. contents::

Deployment Guide
================

This project is not dependent upon any particular web server, app server,
communication protocol, or database backend. However, it is only tested with
certain configurations. Directions for two simple deployments are listed below.

All of the setups listed below require several common pieces of software.
Install the following:

* django-extensions
* django (version 1.6)
* python2
* python2-django-tables2
* python2-factory_boy
* python2-pytz

Development Setup
-----------------

This setup is easy to accomplish. It is suitable for development work, but it
should *not* be used in a production environment.

You do not need to install any additional software for this setup.

Initialize the SQLite database::

    $ apps/manage.py syncdb

Start the server that ships with Django::

    $ apps/manage.py runserver

Direct your web browser to http://localhost:8000/. That's it!

Production Setup
----------------

This setup is harder to accomplish. It is suitable for a small production
environment.

Prerequisites
~~~~~~~~~~~~~

Install the following additional software:

* lighttpd
* mysql
* python2-flup

Web Server
~~~~~~~~~~

Back up your current lighttpd config files. Then, customize and install new
config files::

    # cp /etc/lighttpd/ /etc/lighttpd.old/
    $ vi configs/lighttpd.conf
    $ vi configs/scgi.conf
    # cp -t /etc/lighttpd/ configs/lighttpd.conf configs/scgi.conf
    # systemctl start lighttpd

The lighttpd config files make several important assumtions. For example, they
make assumptions about where the repository has been cloned to (``/srv/http/``)
and which user the web server should run as. Look them over carefully before
installing them.

At this point, the web server should be capable of serving up static files. This
is despite the fact that the django application is not yet working. To determine
whether lighttpd is working, create a file in the ``static`` directory, and
attempt to fetch it::

    $ echo foo > static/testfile
    $ curl localhost/static/testfile
    $ rm static/testfile

This command causes lighttpd to serve a static file directly from the ``static``
folder. If you can fetch this static file, then lighttpd is working.

Database
~~~~~~~~

Edit the ``DATABASES`` section of ``apps/main/settings.py``. When you're done,
it will look something like this::

    DATABASES = {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'elts',
            'USER': 'elts',
            'PASSWORD': 'hackme',
            'HOST': '127.0.0.1',
            'PORT': '',
        }
    }

Install `MySQL-Python`_, then configure the MySQL database::

    $ mysql -p -u root
    mysql> create database elts character set utf8;
    mysql> create user 'elts'@'localhost' IDENTIFIED BY 'hackme';
    mysql> GRANT AlL PRIVILEGES ON elts.* TO 'elts'@'localhost';
    mysql> commit;
    mysql> exit

Initialize the database backend::

    $ apps/manage.py syncdb

This will create all necessary tables in the database.

Application
~~~~~~~~~~~

Generate static files::

    $ apps/manage.py collectstatic

This will search each app in the ``apps`` folder for static resources, such as
CSS files and images, and place those files in the ``static`` folder.

Start the app server (tweak to taste)::

    $ python2 apps/manage.py runfcgi \
        host=127.0.0.1 \
        port=4000 \
        protocol=scgi \
        daemonize=false \
        debug=true

Direct your web browser to http://localhost/. That's it!

Documentation
=============

This file (``README.rst``) is written in reStructuredText format. It can be
compiled to several other formats. To compile it to HTML::

    $ rst2html README.rst > README.html

You can generate documentation about the source code itself using epydoc. For
example::

    $ epydoc \
        --config configs/epydocrc \
        --output <output_dir> \
        $(find apps/ -type f -name '*.py')

graphviz must be installed for epydoc to generate graphs.

You can generate a diagram of the database models::

    $ python2 apps/manage.py graph_models elts | dot -T svg -o elts.svg

Again, graphviz must be installed to generate images.

Static Analysis
===============

You can perform static analysis of individual python files using pylint. Pylint
searches through python code, looking for errors and design issues. To perform
an analysis on the file ``apps/elts/views.py`` with the following command::

    $ pylint \
        --init-hook='import sys; sys.path.append("apps/")' \
        apps/elts/views.py | less

Some warnings are spurious, and you can force pylint to ignore those warnings.
For example, the following might be placed in a models.py file::

    # pylint: disable=R0903
    # "Too few public methods (0/2)"
    # It is both common and OK for a model to have no methods.
    #
    # pylint: disable=W0232
    # "Class has no __init__ method"
    # It is both common and OK for a model to have no __init__ method.

The location of ``pylint: disable=XXXX`` directives is important! For example,
if a "disable" statement is placed at the end of a line, the specified warning
is disabled for only that one line, but if the statement is placed at the top of
a file, the specified warning is ignored throughout that entire file. Don't
apply a "disable" statement to an excessively large scope!

Repository Layout
=================

This section isn't requred reading, but if you really want to understand why the
project is laid out as it is, read on.

apps/
-----

This directory contains django apps. Roughly speaking, a django app is a body of
code that can be installed or removed independently of other django apps.

apps/main/
----------

The "main" app contains project-wide settings. It also contains the root URL
dispatcher. To see where requests are dispatched to, read module
``apps.main.urls``.

apps/elts/
----------

The "elts" app contains everythin necessary for implementing the ELTS lending
system. It contains database models for tracking items, item reservations and
other facts; it provides rules for manipulating those facts; and it provides a
user interface for doing so.

There's one layout quirk of special note. The ``templates`` and ``static``
directories contain yet another directory called ``elts``. It looks something
like this::

    $ tree apps/elts/
    apps/elts/
    |-- __init__.py
    |-- models.py
    |-- static
    |   `-- elts
    |       `-- base.css
    |-- templates
    |   `-- elts
    |       `-- base.html
    |-- tests.py
    |-- urls.py
    `-- views.py

At first glance, this appears redundant. Why not do the following instead? ::

    $ tree apps/elts/
    apps/elts/
    |-- __init__.py
    |-- models.py
    |-- static
    |   `-- base.css
    |-- templates
    |   `-- base.html
    |-- tests.py
    |-- urls.py
    `-- views.py

The latter is a bad idea.

    Now we might be able to get away with putting our templates directly in
    polls/templates (rather than creating another polls subdirectory), but it
    would actually be a bad idea. Django will choose the first template it finds
    whose name matches, and if you had a template with the same name in a
    different application, Django would be unable to distinguish between them.
    We need to be able to point Django at the right one, and the easiest way to
    ensure this is by namespacing them. That is, by putting those templates
    inside another directory named for the application itself.

    -- `Django documentation
    <https://docs.djangoproject.com/en/1.6/intro/tutorial03/#write-views-that-actually-do-something>`__

static
------

The ``static`` folder contains static resources, such as CSS documents or PNG
images. Use the ``collectstatic`` command to populate this directory. The
collectstatic command is described in the `Application`_ section.

Django is good at generating dynamic content, such as HTML documents. However,
it is not good at serving up static files, such as CSS docments or SVG images.
That's the job of a web server, and a web server should serve up resources from
this directory.

The contents of this folder should *not* be version controlled.

configs
-------

Project-wide config files are housed here. Go have a look -- it's pretty
self-explanatory.

sqlite
------

By default, this project uses sqlite as a database backend. This directory
houses that sqlite database file.

The contents of the this folder should *not* be version controlled.

Copyright
=========

ELTS: The Electronic Lending Tracking System
Copyright (C) 2014  Jeremy Audet, Josh Rollet

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.

.. _Django documentation: https://docs.djangoproject.com/en/dev/
.. _MySQL-Python: http://mysql-python.sourceforge.net/

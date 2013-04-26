About
=====

This repo contains the source code for the Electronic Lending Tracking System
(ELTS). ELTS is written using the Django web app framework. If you don't know
Django, go do some reading, then come back. The [The Django
Book](http://www.djangobook.com/en/2.0/index.html) and the official [Django
documentation](https://docs.djangoproject.com/en/dev/) are good references. The
Django Book is old but extremely readable; the Django documentation is
up-to-date but harder to grok.

Deployment Guidelines
=====================

This project is not dependent upon any particular web server, app server,
communication protocol, or database backend. However, it it is tested only with
certain configurations. Directions for setting up specific configurations are
listed below.

### lighttpd + flup + sqlite

Start by installing the following:

* lighttpd
* flup (python 2 version)
* django (python 2 version)
* mysql

Unfortunately, flup (and seemingly every other FastCGI and SCGI handler
available) does not yet support python 3. As a result, the python 2 versions of
flup and django must be used.

Generate static files:

    $ code/manage.py collectstatic

The lighttpd config file assumes that a project branch (such as `trunk`) has
been copied to `/srv/http/`. Tweak the config file if needed, then install it
and start lighttpd.

    $ vi configs/lighttpd.conf
    $ cp configs/lighttpd.conf /etc/lighttpd/lighttpd.conf
    # systemctl start lighttpd

Ensure `collectstatic` collected files and lighttpd is functioning:

    $ curl localhost/static/elts/base.css > /dev/null

Initialize the database backend:

    $ code/manage.py syncdb

Start the app server: (tweak to taste)

    $ python2 code/manage.py runfcgi \
        host=127.0.0.1 \
        port=4000 \
        protocol=scgi \
        daemonize=false \
        debug=true

Test the setup by heading to `localhost/elts/item/` in a web browser. (this page
triggers several database queries, so visiting this page ensures that you've set
things up correctly)

### lighttpd + flup + mysql

Follow directions for setting up lighttpd + flup + sqlite, up to the point where
the database is initialized. Then, edit the `DATABASES` section of
`code/main/settings.py`. When you're done, it will look something like this:

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

Install [MySQL-Python](http://mysql-python.sourceforge.net/), then configure the
MySQL database:

    $ mysql -p -u root
    mysql> create database elts character set utf8;
    mysql> create user 'elts'@'localhost' IDENTIFIED BY 'hackme';
    mysql> GRANT AlL PRIVILEGES ON elts.* TO 'elts'@'localhost';
    mysql> commit;
    mysql> exit
    $ python2.7 code/manage.py syncdb

Start the app server as normal.

Development Guidelines
======================

It is possible to start ELTS with only two commands:

    $ ./manage.py syncdb
    $ ./manage.py runserver

This starts the built-in django webserver and a SQLite database backend. You can
use the setup by heading to `http://localhost:8000/` in a web browser.

Documentation
-------------

The `README.md` file is written in markdown format. It can be compiled to HTML:

    $ markdown README.md > <output_dir>/README.html

You can generate documentation about the source code itself using epydoc. For
example:

    $ epydoc \
        --config configs/epydocrc \
        --output <output_dir> \
        `find code/ -type f -name \*.py`

`graphviz` must be installed for epydoc to generate graphs.

Static Analysis
---------------

You can use pylint to perform static analysis of individual python files. For
example:

    $ pylint --init-hook='import sys; sys.path.append("code/")' code/elts/views.py | less

Some warnings are spurious, and you can force pylint to ignore those warnings.
For example, the following might be placed in a models.py file:

    # pylint: disable=R0903
    # "Too few public methods (0/2)" 
    # It is both common and OK for a model to have no methods.
    #
    # pylint: disable=W0232
    # "Class has no __init__ method" 
    # It is both common and OK for a model to have no __init__ method.

The location of `pylint: diable=XXXX` is important! If "disable" statements are
placed at the top of a file, the named messages are ignored throughout that
entire file, but if they are placed within a class, the named messages are
ignored only within that class. Don't apply a "disable" statement to an
excessively large scope!

Repository Layout
=================

This section isn't requred reading, but if you really want to understand why the
project is laid out as it is, read on.

This project is currently housed in a subversion repository, and the branches,
tags, and trunk folders are used in the usual way. If you don't understand how
branching under subversion works, go do some reading
[here](http://svnbook.red-bean.com/en/1.5/svn.branchmerge.html).

code
----

This directory acts as the root of the django project. Each sub-folder is a
django app.

### code/main

The `main` folder contains project-wide settings and functionas as the "root"
URL dispatcher.

### code/elts

Whereas `main` serves as the "root" project application, `elts` contains all
logic for the actual lending system. Thus, database models for items, item
reservations, tags, and other facts are housed here.

There's one layout quirk of special note. The `templates` and `static`
directories contain yet another directory called `elts`. It looks something like
this:

    $ tree code/elts/
    code/elts/
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

At first glance, this is super awkward. Why not do the following instead?

    $ tree code/elts/
    code/elts/
    |-- __init__.py
    |-- models.py
    |-- static
    |   `-- base.css
    |-- templates
    |   `-- base.html
    |-- tests.py
    |-- urls.py
    `-- views.py

The latter is a bad idea. The django project documentation [explains
why](https://docs.djangoproject.com/en/1.5/intro/tutorial03/#write-views-that-actually-do-something):

> Now we might be able to get away with putting our templates directly in
> polls/templates (rather than creating another polls subdirectory), but it
> would actually be a bad idea. Django will choose the first template it finds
> whose name matches, and if you had a template with the same name in a
> different application, Django would be unable to distinguish between them. We
> need to be able to point Django at the right one, and the easiest way to
> ensure this is by namespacing them. That is, by putting those templates
> inside another directory named for the application itself.

collectstatic
-------------

Django can collect static files such as CSS files into a single, central
location for you. A webserver can then do what it's good at (serving static
files), and django can do what it's good at (generating dynamic content). Run
the `django-admin.py collectstatic` command to collect files into the
`collectstatic` folder. The contents of this folder should *not* be version
controlled.

configs
-------

Project-wide config files are housed here. Go have a look -- it's pretty
self-explanatory.

sqlite
------

By default, this project uses sqlite as a database backend. When you issue
`manage.py syncdb`, a sqlite database file is created in the `sqlite` folder if
necessary, and it is populated with necessary tables. This is great for
development and testing, though it should be changed in production. The contents
of the this folder should *not* be version controlled.

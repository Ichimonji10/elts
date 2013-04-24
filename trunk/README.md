About
=====

This repo contains the source code for the Electronic Lending Tracking System
(ELTS). ELTS is written using the Django web app framework. If you don't know
Django, go do some reading, then come back. The [The Django
Book](http://www.djangobook.com/en/2.0/index.html) and the official [Django
documentation](https://docs.djangoproject.com/en/dev/) are good references.

Repository Layout
=================

This project is currently maintained in a subversion repository, and the
branches, tags, and trunk folders are used in the usual way. If you don't
understand how branching under subversion works, go do some reading
[here](http://svnbook.red-bean.com/en/1.5/svn.branchmerge.html).

Project Layout
==============

code
----

All python code is maintained here. The django documentation details how to
interact with a project using `manage.py`, but here's some highlights:

    $ manage.py syncdb # create database tables
    $ manage.py runserver # run the development webserver

code/main
---------

The `main` folder contains project-wide settings and functionas as the "root"
URL dispatcher.

Django can collect static files, such as CSS files, into a central location for
you. A webserver can then do what it's good at (serving static files), and
django can do what it's good at (generating dynamic content). Run the
`django-admin.py collectstatic` command to collect files into the
`main/collectstatic` folder. The contents of this folder should *not* be
version controlled.

By default, this project uses sqlite as a database backend. When you issue
`manage.py syncdb`, a sqlite database file is created in the `sqlite` folder if
necessary. This is great for development and testing, though it should be
changed in production. The contents of the this folder should *not* be version
controlled.

code/elts
---------

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

Development Guidelines
======================

Documentation
-------------

Use epydoc to generate documentation from the source code itself. For example:

    $ epydoc \
        --config configs/epydocrc \
        --output <output_dir> \
        `find code/ -type f -name \*.py`

`graphviz` must be installed for epydoc to generate graphs.

The `README.md` file is written in markdown format. It can be compiled to HTML:

    $ markdown README.md > <output_dir>/README.html

Static Analysis
---------------

Use pylint to check *every* file. For example:

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

Location is important. If "disable" statements are placed at the top of a file,
the named messages are ignored throughout that entire file, but if they are
placed within a class, the named messages are ignored only within that class.
Don't apply a "disable" statement to an excessively large scope!

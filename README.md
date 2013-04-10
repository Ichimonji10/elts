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

main
----

The `main` folder contains project-wide settings and is the "root" URL
dispatcher. It also contains arbitrary project-wide resources that don't easily
go elsewhere.

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

elts
----

Whereas `main` is dedicated to project-wide resources, `elts` contains all
logic for the actual lending system. Thus, database models for items, item
reservations, tags, and other facts are housed here.

Development Guidelines
======================

Use pylint to check *every* file. For example:

    $ pwd
    .../elts/trunk
    $ pylint --init-hook='import sys; sys.path.append(".")' main/settings.py | less

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

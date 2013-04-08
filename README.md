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

The `elts` folder contains project-wide settings and is the "root" URL
dispatcher. It also contains arbitrary project-wide resources that don't easily
go elsewhere.

Django can collect static files, such as CSS files, into a central location for
you. A webserver can then do what it's good at (serving static files), and
django can do what it's good at (generating dynamic content). Run the
`django-admin.py collectstatic` command to collect files into the
`elts/collectstatic` folder. The contents of this folder should *not* be
version controlled.

By default, this project uses sqlite as a database backend. When you issue
`manage.py syncdb`, a sqlite database file is created in the `sqlite` folder if
necessary. This is great for development and testing, though it should be
changed in production. The contents of the this folder should *not* be version
controlled.

Django apps are placed in the `apps` folder.

=============================
react-comments-django
=============================

Forum and comments application

* Django Rest Framework API
* React application as frontend included
* MathJax support
* Embed Thread component (reactjs + react-bootstrap)
* Comments are ranked using wilson scoring interval and displayed in a tree structure (using `django-mptt <https://github.com/django-mptt/django-mptt>`_)
* Voting functionality for threads & comments
* Compatible with mobile screen sizes
* Users management page for admins (not implemented yet)
* Admins can lock/unlock, edit, delete threads and posts, edit & delete topics (not implemented yet)


Working demo:

Documentation:

Screenshots
-----------

.. image:: https://github.com/physics-is-beautiful/react-comments-django/blob/master/media/drc1.png?raw=true

.. image:: https://github.com/physics-is-beautiful/react-comments-django/blob/master/media/drc2.png?raw=true

Supported Django versions
-------------------------

The app is currently tested with Django 1.8, 1.9, 1.10 and 1.11, 2.0

Quickstart
----------

Install react-comments-django::

    pip install react-comments-django

Add it and its dependencies to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'mptt',
        'react_comments_django',
        ...
        ]

react_comments_django_settings to context_processors:

.. code-block:: python

    'context_processors': [
        ...
        'react_comments_django.context_processors.react_comments_django_settings',
        ...
    ]

react_comments_django's URL patterns:

.. code-block:: python

    from react_comments_django.sitemaps import ThreadSitemap
    from react_comments_django.urls_api import urlpatterns as react_comments_django_urls_api

    sitemaps = {
        'react_comments_django': ThreadSitemap
    }

    urlpatterns = [
        ...
        url(r'^api/v1/', include(react_comments_django_urls_api)),
        url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
        ...
    ]

Migrate models:

.. code-block:: python

    python manage.py migrate react_comments_django


Create a topic:

You can use New Topic dialog in topics page if you're logged in as a superuser or you can create one in a python console:

.. code-block:: python

    from react_comments_django.models import Topic
    Topic.objects.create(title='Test Topic')


Credits
-------

Dependencies:

*  django-mptt_
*  django-ipware_

.. _django-mptt: https://github.com/django-mptt/django-mptt
.. _django-ipware: https://github.com/un33k/django-ipware

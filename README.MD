django-custom-indexes
=====================

Django PostgreSQL backend and custom fields to create custom indexes.

With this, indexes can be defined for a model using field attributes
which will be migrated to the db, this eliminates the need to write
migrations manually with RunSQL to create indexes.

Installation
============

[![](https://img.shields.io/pypi/v/django-custom-indexes.svg)](https://pypi.org/project/django-custom-indexes/) [![](https://img.shields.io/badge/Maintained-yes-green.svg)](https://pypi.org/project/django-custom-indexes/) [![](https://img.shields.io/pypi/djversions/django-custom-indexes.svg)](https://pypi.org/project/django-custom-indexes/) [![](https://img.shields.io/pypi/pyversions/django-custom-indexes.svg)](https://pypi.org/project/django-custom-indexes/)


The package can be installed by running the following command:


    pip install django-custom-indexes

PyPI: https://pypi.python.org/pypi/django-custom-indexes/

Add ``django_custom_indexes`` to your ``INSTALLED_APPS``:


    INSTALLED_APPS = (
        '...',
        'django_custom_indexes'
    )

Requirements:

-  Django 1.7 to 1.11 (not tested for 2.0+).
-  PostgreSQL database backend.
-  Python 2.7

Usage
=====

Creating Indexes in PostgresSQL:
https://www.postgresql.org/docs/9.5/static/sql-createindex.html

In your settings update the ``ENGINE`` parameter of ``DATABASES`` to
``'django_custom_indexes.backends.postgresql_psycopg2'``

By default custom\_indexes backend inherits from
django.db.backends.postgresql\_psycopg2, to use some other sub class of
postgresql\_psycopg2 add the following setting:

``DJANGO_CUSTOM_INDEXES_BASE_ENGINE``

Example Usage:


    from django_custom_indexes import model_fields
    from django.db import models


    class MyModel(models.Model):
        my_field1 = model_fields.CustomCharField(
            max_length=100,
            custom_indexes=[
                {
                    'unique': True, # Optional, used to create unique indexes
                    'name': 'custom_unique_index', # Optional (auto generated), Required only if no columns are specified
                    'where': 'my_field2 > 0', # Optional, used to create partial Indexes
                },
                {
                    'unique': True,
                    'columns': ['lower(my_field1)'], # Optional, Specify columns or expressions for the index
                }
            ]
        )
        my_field2 = model_fields.CustomIntegerField(
            custom_indexes=[
                {
                    'name': 'custom_gin_index1',
                    'using': 'USING gin (my_field2)', # Optional, Specify which method to use for the index
                }
            ]
        )


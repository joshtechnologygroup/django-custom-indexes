import importlib

from django.conf import settings

try:
    # Django >= 1.9
    from django.db.backends.postgresql.base import *

    DEFAULT_BACKEND = 'django.db.backends.postgresql'
except ImportError:
    DEFAULT_BACKEND = 'django.db.backends.postgresql_psycopg2'

from django_custom_indexes.backends.postgresql_psycopg2.schema import DatabaseSchemaEditor


BASE_ENGINE = getattr(settings, 'DJANGO_CUSTOM_INDEXES_BASE_ENGINE', DEFAULT_BACKEND)

BASE_MODULE = importlib.import_module('{}.base'.format(BASE_ENGINE))


class DatabaseWrapper(BASE_MODULE.DatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor

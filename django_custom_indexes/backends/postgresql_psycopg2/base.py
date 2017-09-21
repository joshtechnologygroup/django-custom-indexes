import importlib

from django.conf import settings
from .schema import DatabaseSchemaEditor

BASE_ENGINE = getattr(settings, 'DJANGO_CUSTOM_INDEXES_BASE_ENGINE', 'django.db.backends.postgresql_psycopg2')

BASE_MODULE = importlib.import_module('{}.base'.format(BASE_ENGINE))


class DatabaseWrapper(BASE_MODULE.DatabaseWrapper):
    SchemaEditorClass = DatabaseSchemaEditor

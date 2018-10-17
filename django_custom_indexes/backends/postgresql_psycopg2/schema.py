import importlib

from django.conf import settings

try:
    # Django >= 1.9
    from django.db.backends.postgresql.base import *  # noqa

    DEFAULT_BACKEND = 'django.db.backends.postgresql'
except ImportError:
    DEFAULT_BACKEND = 'django.db.backends.postgresql_psycopg2'

BASE_ENGINE = getattr(settings, 'DJANGO_CUSTOM_INDEXES_BASE_ENGINE', DEFAULT_BACKEND)

BASE_MODULE = importlib.import_module('{}.base'.format(BASE_ENGINE))


class DatabaseSchemaEditor(BASE_MODULE.DatabaseWrapper.SchemaEditorClass):
    sql_create_custom_index = """
        CREATE %(unique)s INDEX %(name)s ON %(table)s %(using)s %(columns)s %(where)s
    """

    def _custom_index_name(self, model, field, index):
        return self.quote_name(self._create_index_name(model, index.get('columns', [field.column]), suffix='_custom'))

    def add_indexes(self, model, field, indexes=None):
        if indexes is None:
            indexes = getattr(field, 'custom_indexes', [])
        for index in indexes:
            columns = ", ".join(index.get('columns', [field.column]))
            name = index.get('name')
            if not name:
                name = self._custom_index_name(model, field, index)
            self.deferred_sql.append(self.sql_create_custom_index % {
                "unique": "UNIQUE" if index.get('unique') else "",
                "name": name,
                "table": self.quote_name(model._meta.db_table),
                "using": index.get('using', ''),
                "columns": "({})".format(columns) if columns else "",
                "where": 'WHERE {}'.format(index.get('where')) if index.get('where') else '',
            })

    def create_model(self, model):
        super(DatabaseSchemaEditor, self).create_model(model)
        for field in model._meta.local_fields:
            self.add_indexes(model, field)

    def add_field(self, model, field):
        super(DatabaseSchemaEditor, self).add_field(model, field)
        self.add_indexes(model, field)

    def _alter_field(self, model, old_field, new_field, old_type, new_type, old_db_params, new_db_params, strict=False):
        super(DatabaseSchemaEditor, self)._alter_field(
            model, old_field, new_field, old_type, new_type, old_db_params, new_db_params, strict
        )
        old_indexes = getattr(old_field, 'custom_indexes', [])
        new_indexes = getattr(new_field, 'custom_indexes', [])
        create_indexes = []
        delete_indexes = []

        if old_indexes != new_indexes:
            for index in new_indexes:
                if index not in old_indexes:
                    create_indexes.append(index)
            for index in old_indexes:
                if index not in new_indexes:
                    delete_indexes.append(index)
        self.add_indexes(model, new_field, create_indexes)

        for index in delete_indexes:
            name = index.get('name', self._custom_index_name(model, old_field, index))
            self.deferred_sql.append(self.sql_delete_index % {"name": name})

from django.core import checks
from django.db import models


class CustomFieldMixin(object):
    def __init__(self, *args, **kwargs):
        self.custom_indexes = kwargs.pop(u'custom_indexes', None)
        super(CustomFieldMixin, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(CustomFieldMixin, self).deconstruct()
        if self.custom_indexes:
            kwargs[u'custom_indexes'] = self.custom_indexes
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super(CustomFieldMixin, self).check(**kwargs)
        errors.extend(self._check_custom_indexes())
        return errors

    def _check_custom_indexes(self):
        if not self.custom_indexes:
            return []
        if not isinstance(self.custom_indexes, list):
            return [
                checks.Error(
                    "'custom_indexes' must be a list.",
                    hint=None,
                    obj=self,
                    id='django_custom_indexes.E001',
                )
            ]
        for index in self.custom_indexes:
            if not isinstance(index, dict):
                return [
                    checks.Error(
                        "Each index must be a dict.",
                        hint=None,
                        obj=self,
                        id='django_custom_indexes.E002',
                    )
                ]
            if not index.get('columns') and not index.get('name'):
                return [
                    checks.Error(
                        "Each index must either have a name or a list of columns",
                        hint=None,
                        obj=self,
                        id='django_custom_indexes.E003',
                    )
                ]
        return []


class CustomAutoField(CustomFieldMixin, models.AutoField):
    pass


class CustomBigIntegerField(CustomFieldMixin, models.BigIntegerField):
    pass


class CustomBinaryField(CustomFieldMixin, models.BinaryField):
    pass


class CustomBooleanField(CustomFieldMixin, models.BooleanField):
    pass


class CustomCharField(CustomFieldMixin, models.CharField):
    pass


class CustomCommaSeparatedIntegerField(CustomFieldMixin, models.CommaSeparatedIntegerField):
    pass


class CustomDateField(CustomFieldMixin, models.DateField):
    pass


class CustomDateTimeField(CustomFieldMixin, models.DateTimeField):
    pass


class CustomDecimalField(CustomFieldMixin, models.DecimalField):
    pass


class CustomDurationField(CustomFieldMixin, models.DurationField):
    pass


class CustomEmailField(CustomFieldMixin, models.EmailField):
    pass


class CustomFileField(CustomFieldMixin, models.FileField):
    pass


class CustomFilePathField(CustomFieldMixin, models.FilePathField):
    pass


class CustomFloatField(CustomFieldMixin, models.FloatField):
    pass


class CustomForeignKey(CustomFieldMixin, models.ForeignKey):
    pass


class CustomForeignObject(CustomFieldMixin, models.ForeignObject):
    pass


class CustomGenericIPAddressField(CustomFieldMixin, models.GenericIPAddressField):
    pass


class CustomIPAddressField(CustomFieldMixin, models.IPAddressField):
    pass


class CustomImageField(CustomFieldMixin, models.ImageField):
    pass


class CustomIntegerField(CustomFieldMixin, models.IntegerField):
    pass


class CustomManyToManyField(CustomFieldMixin, models.ManyToManyField):
    pass


class CustomNullBooleanField(CustomFieldMixin, models.NullBooleanField):
    pass


class CustomOneToOneField(CustomFieldMixin, models.OneToOneField):
    pass


class CustomOrderWrt(CustomFieldMixin, models.OrderWrt):
    pass


class CustomPositiveIntegerField(CustomFieldMixin, models.PositiveIntegerField):
    pass


class CustomPositiveSmallIntegerField(CustomFieldMixin, models.PositiveSmallIntegerField):
    pass


class CustomSlugField(CustomFieldMixin, models.SlugField):
    pass


class CustomSmallIntegerField(CustomFieldMixin, models.SmallIntegerField):
    pass


class CustomTextField(CustomFieldMixin, models.TextField):
    pass


class CustomTimeField(CustomFieldMixin, models.TimeField):
    pass


class CustomURLField(CustomFieldMixin, models.URLField):
    pass


class CustomUUIDField(CustomFieldMixin, models.UUIDField):
    pass

from django.db import models
from django.utils.text import camel_case_to_spaces


class RelatedNameField(models.ForeignKey):
    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        related_name = self.remote_field.related_name
        if not cls._meta.abstract and related_name:
            underscore_name = camel_case_to_spaces(
                cls.__name__
            ).replace(" ", "_")
            self.remote_field.related_name = related_name.format(
                underscore_name=underscore_name
            )


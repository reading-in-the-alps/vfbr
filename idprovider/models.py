from django.db import models


class IdProvider(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_class_name(self):
        class_name = self._meta.model_name
        return class_name

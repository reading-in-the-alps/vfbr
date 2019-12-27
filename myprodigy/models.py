import json
from django.db import models


class Dataset(models.Model):
    name = models.CharField(unique=True, max_length=250)
    created = models.IntegerField()
    meta = models.BinaryField()
    session = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'dataset'

    def __str__(self):
        return f"{self.name}"


class Example(models.Model):
    input_hash = models.BigIntegerField()
    task_hash = models.BigIntegerField()
    content = models.BinaryField()
    link = models.ManyToManyField(Dataset, db_table='link')

    class Meta:
        managed = False
        db_table = 'example'

    def ex_as_json(self):
        return json.loads(self.content.tobytes())

    def __str__(self):
        mytext = self.ex_as_json().get('text')
        return mytext


# class Link(models.Model):
#     example = models.ForeignKey(Example, models.DO_NOTHING)
#     dataset = models.ForeignKey(Dataset, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'link'

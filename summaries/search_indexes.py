import datetime
from haystack import indexes

from . models import VfbEntry, InventoryEntry


class VfbEntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return VfbEntry


class InventoryEntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return InventoryEntry

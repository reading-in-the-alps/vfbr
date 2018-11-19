from django.db import models
from django.urls import reverse

from idprovider.models import IdProvider
from entities.models import Institution, Person, Place
from vocabs.models import SkosConcept


class VerfachBuch(IdProvider):
    """ Beschreibt die Archivalie 'Verfachbuch' """
    signatur = models.CharField(
        max_length=250, blank=True, help_text="Vollzitat des Verfachbuches",
        verbose_name="Archivsignatur des Verfachbuches"
    )
    repo = models.ForeignKey(
        Institution, blank=True, null=True, related_name="has_verfachbuch",
        on_delete=models.SET_NULL,
        verbose_name="Archiv",
        help_text="Das Archiv in welchem das Verfachbuch eingesehen werden kann"
    )
    year = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Jahr",
        help_text="Verfachbuch des Jahres JJJJ"
    )

    def get_next(self):
        next = Verfachbuch.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Verfachbuch.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.signatur:
            return "{}".format(self.signatur)
        else:
            return "{}".format(self.id)


class VfbEntry(IdProvider):
    """Beschreibt einen Eintrag in einem Verfachbuch"""
    entry_signatur = models.CharField(
        max_length=250, blank=True, help_text="Vollzitat des Eintrages",
        verbose_name="Archivsignatur des Eintrages"
    )
    located_in = models.ForeignKey(
        VerfachBuch, blank=True, null=True, related_name="has_entries",
        on_delete=models.SET_NULL,
        verbose_name="Verfachbuch",
        help_text="Das Verfachbuch des Eintrages."
    )
    adm_action_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Art der Amtshandlung",
        help_text="Welche Art von Amtshandlung wurde in diesem Eintrag protokolliert",
        on_delete=models.SET_NULL
    )
    vollregest = models.TextField(
        blank=True, verbose_name="Regest", help_text="Text des Regests"
    )
    mentioned_person = models.ManyToManyField(
        Person,
        max_length=250, blank=True,
        verbose_name="Erwähnte Personen",
        help_text="Identifizierbare Personen, die im Eintrag erwähnt werden.",
        related_name="mentioned_in_entry"
    )
    mentioned_place = models.ManyToManyField(
        Place,
        max_length=250, blank=True,
        verbose_name="Erwähnte Orte",
        help_text="Identifizierbare Orte, die im Eintrag erwähnt werden.",
        related_name="mentioned_in_entry"
    )
    mentioned_institutions = models.ManyToManyField(
        Institution,
        max_length=250, blank=True,
        verbose_name="Erwähnte Institutionen",
        help_text="Identifizierbare Institutionen, die im Eintrag erwähnt werden.",
        related_name="mentioned_in_entry"
    )

    def get_next(self):
        next = VfbEntry.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = VfbEntry.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.entry_signatur:
            return "{}".format(self.entry_signatur)
        else:
            return "{}".format(self.id)

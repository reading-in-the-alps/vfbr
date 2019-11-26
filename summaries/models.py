from django.db import models
from django.urls import reverse

from idprovider.models import IdProvider
from entities.models import Institution, Person, Place
from vocabs.models import SkosConcept

from transkribus.models import TrpBaseModel


class VerfachBuch(IdProvider, TrpBaseModel):
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
        help_text="Verfachbuch des Jahres JJJJ,\
        bei mehreren Jahren wird das frühste Jahr angegeben"
    )
    year_latest = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Jahr",
        help_text="Verfachbuch des Jahres JJJJ,\
        bei mehreren Jahren wird das späteste Jahr angegeben"
    )
    year_label = models.CharField(
        blank=True, null=True,
        max_length=250,
        verbose_name="Jahr(e)",
        help_text="Alle Jahre die das Verfachbuch umfasst"
    )

    @classmethod
    def get_listview_url(self):
        return reverse('summaries:verfachbuecher_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('summaries:verfachbuch_create')

    def get_absolute_url(self):
        return reverse('summaries:verfachbuch_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('summaries:verfachbuch_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('summaries:verfachbuch_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = VerfachBuch.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = VerfachBuch.objects.filter(id__lt=self.id).order_by('-id')
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
    start_page = models.IntegerField(
        blank=True, null=True,
        verbose_name='Blattnummer Eintragsbeginn',
        help_text="Wird zur Sortierung und zur Berechnung des Umfanges des Eintrages verwendet"
    )
    end_page = models.IntegerField(
        blank=True, null=True,
        verbose_name='Blattnummer Eintragsbeginn',
        help_text="Wird zur Sortierung und zur Berechnung des Umfanges des Eintrages verwendet"
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
    inventory = models.BooleanField(
        null=True,
        verbose_name="Inventar",
        help_text="Umfasst der Verfachbucheintrag ein Inventar"
    )
    book = models.BooleanField(
        null=True,
        verbose_name="Bücher",
        help_text="Erwähnt der Verfachbucheintrag Bücher"
    )

    class Meta:
        ordering = [
            'entry_signatur'
        ]

    @classmethod
    def get_listview_url(self):
        return reverse('summaries:verfachbucheintrag_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('summaries:verfachbucheintrag_create')

    def get_absolute_url(self):
        return reverse('summaries:verfachbucheintrag_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('summaries:verfachbucheintrag_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('summaries:verfachbucheintrag_edit', kwargs={'pk': self.id})

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


class Anmerkungen(IdProvider):
    text = models.TextField(
        blank=True, null=True,
        verbose_name="Anmerkung",
        help_text="Anmerkung"
    )
    public = models.BooleanField(
        default=False,
        verbose_name="öffentlich",
        help_text="Soll diese Anmerkung öffentlich Einsehbar sein?"
    )
    entry = models.ForeignKey(
        VfbEntry,
        blank=True, null=True,
        on_delete=models.CASCADE,
        verbose_name="Anmerkung zu Eintrag",
        help_text="Anmerkung/Kommentar zu Eintrag",
        related_name="has_notes"
    )

    @classmethod
    def get_listview_url(self):
        return reverse('summaries:anmerkungen_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('summaries:anmerkung_create')

    def get_absolute_url(self):
        return reverse('summaries:anmerkung_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('summaries:anmerkung_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('summaries:anmerkung_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = Anmerkungen.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Anmerkungen.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return f"{self.text[:20]}"

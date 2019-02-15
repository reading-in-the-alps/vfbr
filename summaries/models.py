from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

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


BUECHER = (
    ('Bücher', 'Bücher'),
    ('keine Bücher', 'keine Bücher'),
)

MEHRERE_HAUPTPERSONEN = (
    ('nur eine Hauptperson', 'nur eine Hauptperson'),
    ('mehrere Personen', 'mehrere Personen')
)

VOLLSTAENDIG = (
    ('unklar', 'unklar'),
    ('unvollständig', 'unvollständig'),
)

SCHREIBUTENSIELIEN = (
    ('Lese- und Schreibsachen', 'Lese- und Schreibsachen'),
    ('keine Lese- und Schreibsachen', 'keine Lese- und Schreibsachen'),
)


class InventoryEntry(IdProvider):
    """Beschreibt ein Regest eines Inventars"""
    inv_signatur = models.CharField(
        max_length=550, blank=True, help_text="Vollzitat des Eintrages",
        verbose_name="Archivsignatur des Eintrages"
    )
    is_located_in = models.ForeignKey(
        VerfachBuch, blank=True, null=True, related_name="has_inventories",
        on_delete=models.SET_NULL,
        verbose_name="Übergeordenter Quellenbestand",
        help_text="Ist Teil des übergordneten Quellenbestands."
    )
    inv_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Art des Inventars",
        help_text="Welche Art von Inventar wurde in diesem Eintrag protokolliert",
        on_delete=models.SET_NULL
    )
    excel_row = JSONField(
        null=True, blank=True, verbose_name="Original Erfassung", help_text="Excel-Sheet Eintrag"
    )
    main_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Name (Erklärung aus Verfachbuch)",
        help_text="Identifizierbare Personen, die im Eintrag erwähnt werden.",
        related_name="is_main_person"
    )
    main_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der Hauptpersonen",
        help_text="Anzahl der Hauptpersonen"
    )
    adm_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Beteiligte (administrative) Personen",
        help_text="Beteiligte Personen (Beamte, Gerichtsverpflichtete, Zeugen, ...).",
        related_name="is_adm_person"
    )
    adm_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl beteiligte (administrative) Personen",
        help_text="Anzahl der beteiligten Personen (Beamte, Gerichtsverpflichtete, Zeugen, ...)"
    )
    related_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Beteiligte (nicht-administrative) Personen",
        help_text="Beteiligte Personen (Erbsinteressenten, Gerhaben, Anweiser,\
        Verkäufer, Verpächter, Käufer, Pächter, ...).",
        related_name="is_related_person"
    )
    related_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der beteiligten (nicht-administrative) Personen",
        help_text="Anzal der beteiligten Personen (Erbsinteressenten, Gerhaben, Anweiser,\
        Verkäufer, Verpächter, Käufer, Pächter, ...)."
    )
    other_person = models.ManyToManyField(
        Person, blank=True,
        verbose_name="Sonstig genannte Personen",
        help_text="Sonstig genannte Personen.",
        related_name="is_other_person"
    )
    other_person_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der sonstig genannten Personen",
        help_text="Anzahl der sonstig genannten Personen"
    )
    barschaft = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Barschaft (teilweise eigene Berechnung)",
        help_text="Barschaft (teilweise eigene Berechnung)"
    )
    invenatar_summe_norm_fl = models.IntegerField(
        blank=True, null=True,
        verbose_name="Inventarsumme normiert (Gulden)",
        help_text="Inventarsumme normiert (Gulden)"
    )
    invenatar_summe_norm_kr = models.FloatField(
        blank=True, null=True,
        verbose_name="Inventarsumme normiert (Kreuzer)",
        help_text="Inventarsumme normiert (Kreuzer)"
    )
    vor_passiva_fl = models.IntegerField(
        blank=True, null=True,
        verbose_name="vor Abzug Passiva (Gulden)",
        help_text="vor Abzug Passiva (Gulden)"
    )
    vor_passiva_kr = models.FloatField(
        blank=True, null=True,
        verbose_name="vor Abzug Passiva (Kreuzer)",
        help_text="vor Abzug Passiva (Kreuzer)"
    )
    nach_passiva_fl = models.IntegerField(
        blank=True, null=True,
        verbose_name="nach Abzug Passiva (Gulden)",
        help_text="nach Abzug Passiva (Gulden)"
    )
    nach_passiva_kr = models.FloatField(
        blank=True, null=True,
        verbose_name="nach Abzug Passiva (Kreuzer)",
        help_text="nach Abzug Passiva (Kreuzer)"
    )
    comment_b = models.TextField(
        blank=True, null=True,
        verbose_name="Kommentar zu Spalte B",
        help_text="Kommentar zu Spalte B"
    )
    comment_k = models.TextField(
        blank=True, null=True,
        verbose_name="Kommentar zu Spalte K",
        help_text="Kommentar zu Spalte K"
    )
    comment_a = models.TextField(
        blank=True, null=True,
        verbose_name="Kommentar zu Spalte A",
        help_text="Kommentar zu Spalte A"
    )
    only_one_person = models.CharField(
        blank=True, null=True, default="mehrere Personen",
        choices=MEHRERE_HAUPTPERSONEN, max_length=250,
        verbose_name="Eine oder mehrere Hauptpersonen?"
    )
    buecher = models.TextField(
        blank=True, null=True,
        verbose_name="Buch/Bücher",
        help_text="Buch/Bücher"
    )
    buecher_sys = models.CharField(
        blank=True, null=True, default="keine Bücher",
        choices=BUECHER, max_length=250,
        verbose_name="Bücher erwähnt?"
    )
    vollstaendig = models.CharField(
        blank=True, null=True, default="unklar",
        verbose_name="Inventar vollständig?",
        choices=VOLLSTAENDIG, max_length=250,
    )

    @classmethod
    def get_listview_url(self):
        return reverse('summaries:inventory_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('summaries:inventory_create')

    def get_absolute_url(self):
        return reverse('summaries:inventory_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('summaries:inventory_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('summaries:inventory_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = InventoryEntry.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = InventoryEntry.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.inv_signatur:
            return "{}".format(self.inv_signatur)
        else:
            return "{}".format(self.id)

    def save_stats(self, *args, **kwargs):
        self.main_person_nr = self.main_person.all().count()
        self.adm_person_nr = self.adm_person.all().count()
        self.related_person_nr = self.related_person.all().count()
        self.other_person_nr = self.other_person.all().count()
        self.save()


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
    inventory = models.BooleanField(
        null=True,
        verbose_name="Inventar",
        help_text="Umfasst der Verfachbucheintrag ein Inventar"
    )

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

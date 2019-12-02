from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

from books.models import Work
from idprovider.models import IdProvider
from entities.models import Institution, Person, Place
from vocabs.models import SkosConcept

from transkribus.models import TrpBaseModel


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
        related_name="adm_action_type_of_vfbentry",
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
    inventory_entry = models.ForeignKey(
        'InventoryEntry', blank=True, null=True,
        verbose_name="Inventar Zusammenfassung",
        help_text="Systematische Beschreibung des Eintrages",
        related_name="has_vfb_entry",
        on_delete=models.SET_NULL
    )
    book = models.BooleanField(
        null=True,
        verbose_name="Bücher",
        help_text="Erwähnt der Verfachbucheintrag Bücher"
    )
    trp_page_nr_start = models.CharField(
            max_length=250, blank=True, help_text="Seitenzahl (Beginn)",
            verbose_name="Beginn (Seitenzahl) des Transkribus Dokuments"
    )
    trp_page_nr_end = models.CharField(
            max_length=250, blank=True, help_text="Seitenzahl (Ende)",
            verbose_name="Ende (Seitenzahl) des Transkribus Dokuments"
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

    def get_facs_link(self):
        try:
            url = reverse(
                'transkribus:trp_page',
                kwargs={
                    'col_id': self.located_in.col_id,
                    'doc_id': self.located_in.doc_id,
                    'page_id': self.trp_page_nr_start
                }
            )
        except Exception as e:
            url = False
        return url

    def __str__(self):
        if self.entry_signatur:
            return "{}".format(self.entry_signatur)
        else:
            return "{}".format(self.id)


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
    mentioned_books = models.ManyToManyField(
        Work, blank=True,
        verbose_name="Erwähnte Bücher",
        help_text="Bücher, die in den Inventaren erwähnt wurden",
        related_name="is_related_work"
    )
    mentioned_books_nr = models.IntegerField(
        blank=True, null=True,
        verbose_name="Anzahl der erwähnten Bücher",
        help_text="Anzahl der erwähnten Bücher"
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
        if int(self.main_person_nr) == 1:
            self.only_one_person = "nur eine Hauptperson"
        self.save()


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

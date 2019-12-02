from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

from vocabs.models import SkosConcept
from entities.models import Place
from idprovider.models import IdProvider

from . utils import lobid_to_data, get_results, query_bsb, sanitize_querystring


class Creator(IdProvider):
    """Beschreibt einen Akteur der für die Erzeugung eines Werkes verantwortlich war."""
    legacy_id = models.CharField(
        max_length=250, blank=True,
        verbose_name="Lokale ID",
        help_text="Lokaler Identifier (rita.acdh.oeaw.ac.at)"
    )
    name = models.CharField(
        max_length=250, blank=True,
        verbose_name="Name",
        help_text="Normalisierte Namensansetzung"
    )
    normdata_id = models.CharField(
        max_length=350, blank=True,
        verbose_name="Normdaten ID",
        help_text="Link zu Normdateneintrag"
    )
    creator_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Gewissheit (Titel)",
        help_text="Wie sicher ist es, dass genau dieser Erzeuger gemeint war",
        on_delete=models.SET_NULL
    )
    gnd_date_of_death = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Todesdatum",
        help_text="Todesdatum (aus GND übernommen und auf YYYY-01-01 normalisiert."
    )
    gnd_geographic_area = models.ManyToManyField(
        Place, blank=True,
        verbose_name="Wirkungsort(e)",
        help_text="Wirkungsort(e) (aus GND übernommen)",
        related_name="has_creator"
    )
    gnd_data = JSONField(
        null=True, blank=True, verbose_name="GND Daten", help_text="Daten aus der GND"
    )

    def __str__(self):
        return "{}".format(self.name)

    def get_lobid_rdf(self):
        if self.normdata_id.startswith('http'):
            gnd_id = self.normdata_id.split('/')[-1]
            lobid_url = settings.LOBID_JSON.format(gnd_id)
        else:
            lobid_url = None
        if lobid_url is not None:
            data = lobid_to_data(lobid_url)
            if data is not None:
                self.gnd_data = data
                self.save()
                return data
            else:
                return None

    @classmethod
    def get_listview_url(self):
        return reverse('books:creator_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('books:creator_create')

    def get_absolute_url(self):
        return reverse('books:creator_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('books:creator_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('books:creator_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('books:creator_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'books:creator_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'books:creator_detail',
                kwargs={'pk': prev.first().id}
            )
        return False


class Work(IdProvider):
    legacy_id = models.CharField(
        max_length=250, blank=True,
        verbose_name="Lokale ID",
        help_text="Lokaler Identifier (rita.acdh.oeaw.ac.at)"
    )
    title = models.CharField(
        max_length=450, blank=True,
        verbose_name="Titel",
        help_text="(Normalisierter) Titel des Werkes"
    )
    creator = models.ManyToManyField(
        Creator, blank=True,
        verbose_name="Erzeuger",
        help_text="Person oder Institution die an der Erzeugung des Werkes beteiligt waren.",
        related_name="has_creator"
    )
    year_of_origin = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Erscheinungsjahr",
        help_text="Jahr der Erstveröffentlichung"
    )
    title_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Gewissheit (Titel)",
        help_text="Wie sicher ist die Titelansetzung",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{}".format(self.title)

    @classmethod
    def get_listview_url(self):
        return reverse('books:work_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('books:work_create')

    def get_absolute_url(self):
        return reverse('books:work_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('books:work_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('books:work_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('books:work_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'books:work_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'books:work_detail',
                kwargs={'pk': prev.first().id}
            )
        return False


class Exemplar(IdProvider):
    normdata_id = models.CharField(
        max_length=350, blank=True,
        verbose_name="Normdaten ID",
        help_text="Link zu Normdateneintrag"
    )
    certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Gewissheit",
        help_text="Wie sicher ist diese Verbindung",
        on_delete=models.SET_NULL
    )
    related_work = models.ForeignKey(
        Work, blank=True, null=True,
        verbose_name="Werk",
        help_text="Werk",
        related_name="has_exemplar",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        if self.normdata_id:
            return "{}".format(self.normdata_id)
        else:
            return "{}".format(self.id)

    @classmethod
    def get_listview_url(self):
        return reverse('books:exemplar_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('books:exemplar_create')

    def get_absolute_url(self):
        return reverse('books:exemplar_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('books:exemplar_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('books:exemplar_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('books:exemplar_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'books:exemplar_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'books:exemplar_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def get_bvb_id(self):
        if self.normdata_id.startswith('http://mdz-nbn-resolving.de'):
            try:
                bsb_id = self.normdata_id.split(settings.BSB_PATTERN)[1]
            except IndexError:
                bsb_id = None
            return bsb_id

    def get_rdf(self):
        if self.get_bvb_id() is not None:
            query = sanitize_querystring(query_bsb, self.get_bvb_id())
            results = get_results(query)
            return results

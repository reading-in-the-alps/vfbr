import re
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from idprovider.models import IdProvider

from browsing.browsing_utils import model_to_dict
from vocabs.models import SkosConcept

from . utils import get_coordinates


class AlternativeName(IdProvider):
    name = models.CharField(
        max_length=250, blank=True, help_text="Alternative Name"
    )

    def get_next(self):
        next = AlternativeName.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = AlternativeName.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return "{}".format(self.name)


class Place(IdProvider):
    PLACE_TYPES = (
        ("city", "city"),
        ("country", "country")
    )

    """Holds information about entities."""
    name = models.CharField(
        max_length=250, blank=True,
        verbose_name="Ortsname",
        help_text="Normalisierte Namensansetzung"
    )
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names",
        related_name="altname_of_place"
    )
    geonames_id = models.CharField(
        max_length=50, blank=True,
        help_text="GND-ID"
    )
    lat = models.DecimalField(
        max_digits=20, decimal_places=12,
        blank=True, null=True
    )
    lng = models.DecimalField(
        max_digits=20, decimal_places=12, blank=True, null=True
    )
    part_of = models.ForeignKey(
        "Place", null=True, blank=True,
        help_text="A place (country) this place is part of.",
        related_name="has_child",
        on_delete=models.SET_NULL
    )
    place_type = models.CharField(
        choices=PLACE_TYPES, null=True, blank=True, max_length=50
    )

    def get_geonames_url(self):
        if self.geonames_id:
            geo_id = re.findall(r'\d+', f"{self.geonames_id}")[0]
            print(geo_id)
            return "https://www.geonames.org/{}".format(geo_id)

    def get_geonames_rdf(self):
        try:
            number = re.findall(r'\d+', str(self.geonames_id))[0]
            return number
        except Exception as e:
            return None

    def save(self, *args, **kwargs):
        if self.geonames_id:
            new_id = self.get_geonames_url()
            self.geonames_id = new_id
        if self.get_geonames_rdf() and not self.lat:
            coords = get_coordinates(self.get_geonames_rdf())
            if coords:
                self.lat = coords['lat']
                self.lng = coords['lng']
        super(Place, self).save(*args, **kwargs)

    @classmethod
    def get_listview_url(self):
        return reverse('entities:place_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:place_create')

    def get_absolute_url(self):
        return reverse('entities:place_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:place_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:place_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'entities:place_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:place_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def __str__(self):
        return "{}".format(self.name)


class Institution(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(max_length=300, blank=True)
    authority_url = models.CharField(max_length=300, blank=True)
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names",
        related_name="altname_of_inst"
    )
    abbreviation = models.CharField(max_length=300, blank=True)
    location = models.ForeignKey(
        Place, blank=True, null=True, on_delete=models.SET_NULL
    )
    parent_institution = models.ForeignKey(
        'Institution', blank=True, null=True, related_name='children_institutions',
        on_delete=models.SET_NULL
    )
    comment = models.TextField(blank=True)

    @classmethod
    def get_listview_url(self):
        return reverse('entities:institution_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:institution_create')

    def get_absolute_url(self):
        return reverse('entities:institution_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:institution_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:institution_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'entities:institution_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:institution_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def __str__(self):
        return "{}".format(self.written_name)


GENDER = (
    ('männlich', 'männlich'),
    ('weiblich', 'weiblich'),
    ('anders', 'anders'),
)


class Person(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True)
    written_name = models.CharField(
        max_length=300, blank=True,
        verbose_name="Umfassende Namensansetzung",
        help_text="Eine möglichst umfassende Namensansetzung mit deren Hilfe es möglich sein sollte, die Person eindeutig zu identifizieren."
    )
    written_name_leven = models.CharField(max_length=254, blank=True)
    forename = models.CharField(
        max_length=300, blank=True,
        verbose_name="Vorname",
        help_text="Vorname"
    )
    name = models.CharField(
        max_length=300, blank=True,
        verbose_name="Nachnname",
        help_text="Nachnname"
    )
    gender = models.CharField(
        max_length=300, blank=True,
        verbose_name="Geschlecht", choices=GENDER
    )
    house_name = models.CharField(max_length=300, blank=True)
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250, blank=True,
        help_text="Alternative names",
        related_name="altname_of_persons"
    )
    profession = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="Beruf(e)",
        related_name="is_profession_of"
    )
    belongs_to_place = models.ManyToManyField(
        Place, blank=True,
        related_name="living_place_for",
        verbose_name="Wohn- und Wirkungsort(e)",
    )
    place_of_birth = models.ForeignKey(
        Place, blank=True, null=True, related_name="is_birthplace",
        verbose_name="Geburtsort",
        on_delete=models.SET_NULL
    )
    place_of_death = models.ForeignKey(
        Place, blank=True, null=True, related_name="is_deathplace",
        verbose_name="Sterbeort",
        on_delete=models.SET_NULL
    )
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Geburtsdatum",
        help_text="YYYY-MM-DD"
    )
    date_of_death = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True,
        verbose_name="Sterbedatum",
        help_text="YYYY-MM-DD"
    )
    belongs_to_institution = models.ForeignKey(
        Institution, blank=True, null=True, related_name="has_member",
        on_delete=models.SET_NULL
    )
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    @classmethod
    def get_listview_url(self):
        return reverse('entities:person_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:person_create')

    def get_absolute_url(self):
        return reverse('entities:person_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('entities:person_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:person_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:person_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'entities:person_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:person_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

    def field_dict(self):
        return model_to_dict(self)

    def get_family(self):
        ct = ContentType.objects.get(app_label='entities', model='personperson').model_class()
        active = ct.objects.filter(source=self)
        inverse = ct.objects.filter(target=self)
        return {
            "active": active,
            "inverse": inverse
        }

    def __str__(self):
        if self.written_name:
            return "{}".format(self.written_name)
        elif self.name and self.forename:
            return "{}, {}".format(self.name, self.forename)
        elif self.name:
            return "{}".format(self.name)
        else:
            return "No name provided"


class PersonPerson(IdProvider):
    source = models.ForeignKey(
        Person, blank=True, null=True,
        related_name="has_person_a",
        verbose_name="Person A",
        on_delete=models.SET_NULL
    )
    target = models.ForeignKey(
        Person, blank=True, null=True,
        related_name="has_person_b",
        verbose_name="Person B",
        on_delete=models.SET_NULL
    )
    rel_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Art der Verbindung",
        related_name="relation_type",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "{} {} {}".format(self.source, self.rel_type, self.target)

    @classmethod
    def get_listview_url(self):
        return reverse('entities:personperson_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('entities:personperson_create')

    def get_absolute_url(self):
        return reverse('entities:personperson_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('entities:personperson_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('entities:personperson_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('entities:personperson_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id).order_by('id')
        if next:
            return reverse(
                'entities:personperson_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'entities:personperson_detail',
                kwargs={'pk': prev.first().id}
            )
        return False

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from measurement.measures import Mass, Volume, Distance
from djmoney.models.fields import MoneyField


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class DefaultBaseModel(TimestampedModel):
    slug = models.SlugField(max_length=36, unique=True, null=False, blank=False)

    def save(self, **kwargs):
        if not self.id:
            self.slug = uuid.uuid4()

        super(DefaultBaseModel, self).save(**kwargs)

    class Meta:
        abstract = True


class CSVFile(DefaultBaseModel):
    title = models.CharField(max_length=70, blank=True, null=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    parsed = models.NullBooleanField()

    def __str__(self):
        return '{} - {}'.format(self.slug, self.file.name)

    class Meta:
        ordering = ['slug']
        verbose_name = _('.csv File')
        verbose_name_plural = _('.csv Files')


class Measure(DefaultBaseModel):
    MEASURE_CHOICES = {
        'quilogramas': (_('{}{}'.format(Mass.SI_PREFIXES.get('kilo'), Mass.ALIAS.get('gram'))), _('kilogram')),
        'litros': (_('{}'.format(Volume.ALIAS.get('litre'))), _('litre')),
        'metros': (_('{}'.format(Distance.ALIAS.get('meter'))), _('meter')),
        'peças': (_('piece'), _('piece')),
        'unidades': (_('unit'), _('unit')),
    }
    measure = models.CharField(max_length=6, blank=False, null=False, choices=MEASURE_CHOICES.values())

    def __str__(self):
        return '{}'.format(self.measure)

    class Meta:
        verbose_name = _('Measure')


class Bag(DefaultBaseModel):
    residue_name = models.CharField(max_length=140, blank=False, null=False, verbose_name=_('Residue Name'))
    price = MoneyField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name=_('Price'),
                       default_currency='BRL')
    quantity = models.IntegerField(blank=False, null=True, verbose_name=_('Quantity'))
    measure = models.ForeignKey(Measure, related_name='bags_measure', on_delete=models.CASCADE, to_field='slug',
                                verbose_name=_('Measure'))
    csv_file = models.ForeignKey(CSVFile, related_name='bags_csv_file', on_delete=models.CASCADE, to_field='slug',
                                 verbose_name=_('CSV File'))
    created_at = models.DateField()

    def __str__(self):
        return '{} - {}'.format(self.residue_name, self.measure)

    class Meta:
        ordering = ['residue_name']
        verbose_name = _('Bag')

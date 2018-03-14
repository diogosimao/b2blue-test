import csv

from logging import getLogger
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from background_task import background
from djmoney.money import Money
from dateparser import parse

from apps.bags.models import CSVFile, Bag, Measure


logger = getLogger(__name__)


def get_file_content_as_dict(file_path):
    return csv.DictReader(open(file_path, 'r'))


def get_unit_as_instance(unit_name):
    unit_name = unit_name.strip().lower()
    unit = Measure.MEASURE_CHOICES.get(unit_name)
    if isinstance(unit, tuple):
        unit_name = unit[0]
    else:
        return None

    created = Measure.objects.get_or_create(measure=unit_name)

    if created:
        return Measure.objects.get(measure=unit_name)

    return None


def get_created_from_str(created_at_str):
    return created_at_str


@background(schedule=1)
def bag_insertion(file_id):
    csv_file_instance = CSVFile.objects.filter(parsed__isnull=True, id=file_id).first()
    if not csv_file_instance:
        logger.debug(_('No CSVFile instance inserted in order to parse'))
        return False

    dict_content = get_file_content_as_dict(csv_file_instance.file.name)

    error = False
    for row in dict_content:
        logger.info(row['Residuo'], row['Quantidade'], row['Unidade'], row['Preco'], row['Data criacao'])
        unit_instance = get_unit_as_instance(row['Unidade'])

        if not isinstance(unit_instance, Measure):
            error = True
            logger.error(_('Invalid measurement unit'))
            break

        created_at = parse(row['Data criacao'], date_formats=['%d de %B de %Y'], languages=['pt'])
        price = row['Preco'].replace(',', '.')
        try:
            quantity = int(row['Quantidade'])
        except ValueError:
            quantity = None
        residue_name = row['Residuo']

        bag_instance = Bag(residue_name=residue_name,
                           price=Money(price, 'BRL'),
                           quantity=quantity,
                           measure=unit_instance,
                           csv_file=csv_file_instance,
                           created_at=created_at if created_at else datetime.today()
                           )
        bag_instance.save()

    if error:
        csv_file_instance.parsed = False
        csv_file_instance.save()
        return False

    csv_file_instance.parsed = True
    csv_file_instance.save()
    return True

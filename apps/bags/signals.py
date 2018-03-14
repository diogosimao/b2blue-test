from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import CSVFile
from .tasks import bag_insertion


@receiver(post_save, sender=CSVFile)
def add_bag_task(sender, instance, **kwargs):
    bag_insertion(instance.id)

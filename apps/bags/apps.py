from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BagsConfig(AppConfig):
    name = 'apps.bags'
    verbose_name = _('Bags')

    def ready(self):
        import apps.bags.signals

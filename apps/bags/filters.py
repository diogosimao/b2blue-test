import django_filters
from django_filters.widgets import RangeWidget

from .models import Bag


class BagFilter(django_filters.FilterSet):
    residue_name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.RangeFilter(widget=RangeWidget())
    created_at = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Bag
        fields = ['measure']

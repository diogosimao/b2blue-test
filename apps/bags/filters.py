import django_filters
from django import forms

from .models import Bag


class BagFilter(django_filters.FilterSet):
    residue_name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter(field_name='price',
                                        widget=forms.NumberInput(attrs={'id': 'id_price_slider',
                                                                        'hidden': True,
                                                                        'data-slider-min': '10',
                                                                        'data-slider-max': '1000',
                                                                        'data-slider-step': '5',
                                                                        'data-slider-value': '[250,450]'}))
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte',
                                             widget=forms.NumberInput(attrs={'hidden': True}), label='')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte',
                                             widget=forms.NumberInput(attrs={'hidden': True}), label='')
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte',
                                                    widget=forms.DateInput(
                                                        attrs={'class': 'datepicker ', 'type': 'date'}),)
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte',
                                                    widget=forms.DateInput(
                                                        attrs={'class': 'datepicker', 'type': 'date'}),)

    class Meta:
        model = Bag
        fields = ['measure']

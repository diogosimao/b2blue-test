from django.shortcuts import render

from .filters import BagFilter
from .models import Bag


def bag_list(request):
    f = BagFilter(request.GET, queryset=Bag.objects.all())
    return render(request, 'bags/reports.html', {'filter': f})

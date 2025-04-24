import django_filters 
from django.db.models import Q

from common import models 


class ClientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')
    is_new = django_filters.BooleanFilter(method='filter_by_new')

    class Meta:
        model = models.Client
        fields = ['region', 'is_new', 'search']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(code_number__icontains=value) |
            Q(numbers__number__icontains=value)
        ).distinct()
    
    def filter_by_new(self, querysey, name, value):
        return querysey.filter(
            orders__status='yangi'
        )
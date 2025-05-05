import django_filters 
from django.db.models import Q

from common import models 


class ClientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')
    is_new = django_filters.BooleanFilter(method='filter_by_new')
    client_type = django_filters.CharFilter(method='filter_by_client_type')
    number_of_trips = django_filters.CharFilter(method='filter_by_number_of_trips')

    class Meta:
        model = models.Client
        fields = ['region', 'is_new', 'search', 'client_type', 'number_of_trips']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(code_number__icontains=value) |
            Q(numbers__number__icontains=value)
        ).distinct()
    
    def filter_by_new(self, queryset, name, value):
        return queryset.filter(
            orders__status=['new', 'cancelled']
        )
    
    def filter_by_client_type(self, queryset, name, value):
        if value:
            return queryset.filter(
                client_type=value
            )
        else:
            return queryset
    
    def filter_by_number_of_trips(self, queryset, name, value):
        if value:
            return queryset.filter(
                region__number_of_trips=value
            )
        else:
            return queryset
import django_filters 
from common import models 


class ClientFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(field_name='full_name', lookup_expr='icontains')
    code_number = django_filters.CharFilter(field_name='code_number', lookup_expr='icontains')
    phone_numbers = django_filters.CharFilter(field_name='numbers__number', lookup_expr='icontains')

    class Meta:
        model = models.Client
        fields = ['region', 'orders__status', 'full_name', 'code_number', 'phone_numbers']
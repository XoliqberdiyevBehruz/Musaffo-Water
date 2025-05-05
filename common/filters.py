import django_filters 
from django.db.models import Q

from common import models, serializers


class ClientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all')
    is_new = django_filters.BooleanFilter(method='filter_by_new')
    client_type = django_filters.CharFilter(method='filter_by_client_type')
    number_of_trips = django_filters.CharFilter(method='filter_by_number_of_trips')
    is_delivered = django_filters.BooleanFilter(method='filter_by_is_delivered')
    number = django_filters.NumberFilter(method='filter_by_number')

    class Meta:
        model = models.Client
        fields = ['region', 'is_new', 'search', 'client_type', 'number_of_trips', 'is_delivered', 'number']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(code_number__icontains=value) |
            Q(numbers__number__icontains=value)
        ).distinct()
    
    def filter_by_new(self, queryset, name, value):
        if value == True:
            return queryset.filter(
                Q(orders__status='new',) |
                Q(orders__status='cancelled')
            )
        else:
            return queryset
    
    def filter_by_is_delivered(self, queryset, name, value):
        if value == True:
            return queryset.filter(
                orders__status='delivered'
            )
        return queryset
    
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
        
    def filter_by_number(self, queryset, name, value):
        clients = queryset.distinct()
        count = 0
        result = []
        for client in clients:
            order = client.orders.filter(count__lte=value).order_by('-created_at').first()
            print(order)
            print(count + order.count < value)
            if  count + order.count <= value:
                count += order.count
                result.append(client.pk)
                print("yesssssss")
            if not order:
                continue
            if order.count == value:
                count += order.count
                result.append(client.pk)
                print('yess')
            else:
                continue
    
            if count == value:
                break
        return queryset.filter(pk__in=result)
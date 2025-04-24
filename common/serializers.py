from django.db import transaction
from django.db.models import Sum

from rest_framework import serializers

from common import models 


class ClientCreateSerializer(serializers.Serializer):
    code_number = serializers.IntegerField()
    full_name = serializers.CharField()
    region = serializers.IntegerField()
    location_text = serializers.CharField()
    cooler = serializers.CharField()
    phone_numbers = serializers.ListSerializer(child=serializers.CharField())
    order_count = serializers.IntegerField()
    price = serializers.IntegerField()
    paid = serializers.IntegerField()
    indebtedness = serializers.IntegerField()

    def validate_region(self, region):
        try:
            region = models.Region.objects.get(id=region)
        except:
            raise serializers.ValidationError('region not found')
        return region 
    

    def create(self, validated_data):
        with transaction.atomic():
            client = models.Client.objects.create(
                full_name=validated_data['full_name'],
                code_number=validated_data['code_number'],
                region=validated_data['region'],
                location_text=validated_data['location_text'],
                cooler=validated_data['cooler'],    
            )  
            for phone in validated_data['phone_numbers']:
                models.ClientPhoneNumber.objects.create(number=phone, client=client)
            
            order = models.Order.objects.create(
                client=client,
                count=validated_data['order_count'],
                price=validated_data['price'],
                indebtedness=validated_data['indebtedness'],
                paid=validated_data['paid'],
                the_rest=validated_data['order_count']
            )
            return order
        
    
class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ['id', 'name']


class ClientOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'id', 'count', 'price', 'received', 'the_rest', 'paid', 'indebtedness', 'status', 'created_at'
        ]



class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'id', 'count', 'price', 'the_rest', 'indebtedness',
        ]
    


class ClientOrderCreateSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    count = serializers.IntegerField()
    price = serializers.IntegerField()
    the_rest = serializers.IntegerField(required=False)
    received = serializers.IntegerField(required=False)
    paid = serializers.IntegerField(required=False)
    indebtedness = serializers.IntegerField(required=False)

    def validate_client_id(self, client_id):
        try:
            client = models.Client.objects.get(id=client_id)
        except models.Client.DoesNotExist:
            raise serializers.ValidationError('client not found')
        return client
    
    def create(self, validated_data):
        with transaction.atomic():
            # last_order = models.Order.objects.filter(client=validated_data['client_id']).order_by('-created_at').first()
            # if last_order:
            order = models.Order.objects.create(
                client=validated_data['client_id'],
                count=validated_data['count'],
                price=validated_data['price'],
                the_rest=validated_data['count'],
                received=validated_data['received'],
                paid=validated_data['paid'],
                indebtedness=validated_data['indebtedness'],
            )
            # else:
            #     order = models.Order.objects.create(
            #         client=validated_data['client_id'],
            #         count=validated_data['count'],
            #         price=validated_data['price'],
            #         the_rest=validated_data['count'],
            #         received=validated_data['received'],
            #         paid=validated_data['paid'],
            #         indebtedness=validated_data['indebtedness'],
            #     )
            return ClientOrderListSerializer(order).data
        

class ClientPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientPhoneNumber
        fields = [
            'id', 'number'
        ]


class ClientDetailSerializer(serializers.ModelSerializer):
    region = RegionListSerializer()
    numbers = serializers.SerializerMethodField(method_name='get_numbers')
    orders_count = serializers.SerializerMethodField(method_name='get_orders_count')
    empty_dish = serializers.SerializerMethodField(method_name='get_empty_dish')
    all_debt = serializers.SerializerMethodField(method_name='get_all_debt')

    class Meta:
        model = models.Client
        fields = [
            'id', 'code_number', 'full_name', 'region', 'numbers', 'cooler', 'location_text', 'orders_count', 'empty_dish', 'all_debt'
        ]

    def get_numbers(self, obj):
        numbers = models.ClientPhoneNumber.objects.filter(client=obj)
        return ClientPhoneNumberSerializer(numbers, many=True).data
    
    def get_orders_count(self, obj):
        return models.Order.objects.filter(client=obj).count()
    
    def get_empty_dish(self, obj):
        return models.Order.objects.filter(client=obj).aggregate(
            empty_dish=Sum('the_rest')
        )
        
    def get_all_debt(self, obj):
        return models.Order.objects.filter(client=obj).aggregate(
            all_debt=Sum('indebtedness')
        )



class ClientListSerializer(serializers.ModelSerializer):
    region = RegionListSerializer()
    numbers = serializers.SerializerMethodField(method_name='get_numbers')
    order = serializers.SerializerMethodField(method_name='get_order')

    class Meta:
        model = models.Client
        fields = [
            'id', 'code_number', 'full_name', 'region', 'numbers', 'cooler', 'location_text', 'order',
        ]

    def get_numbers(self, obj):
        numbers = models.ClientPhoneNumber.objects.filter(client=obj)
        return ClientPhoneNumberSerializer(numbers, many=True).data
    
    def get_order(self, obj):
        order =  models.Order.objects.filter(client=obj).last()
        return OrderListSerializer(order).data



class ClientUpdateSerializer(serializers.ModelSerializer):
    numbers = ClientPhoneNumberSerializer(many=True)

    class Meta:
        model = models.Client
        fields = [
            'code_number', 'full_name', 'region', 'numbers', 'cooler', 'location_text'
        ]


    def update(self, instance, validated_data):
        numbers_data = validated_data.pop('numbers', [])

        instance.code_number = validated_data.get('code_number', instance.code_number)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.region = validated_data.get('region', instance.region)
        instance.cooler = validated_data.get('cooler', instance.cooler)
        instance.location_text = validated_data.get('location_text', instance.location_text)
        models.ClientPhoneNumber.objects.filter(client=instance).delete()
        for number_data in numbers_data:
            models.ClientPhoneNumber.objects.update_or_create(client=instance, number=number_data['number'])
        instance.save()
        return instance
    

class ClientOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'count', 'price', 'the_rest', 'received', 'paid', 'indebtedness', 'status',
        ]

    def update(self, instance, validated_data):
        instance.count = validated_data.get('count', instance.count)
        instance.price = validated_data.get('price', instance.price)
        instance.received = validated_data.get('received', instance.received)
        instance.paid = validated_data.get('paid', instance.paid)
        instance.status = validated_data.get('status', instance.status)
        instance.the_rest = validated_data.get('count', instance.count) - (validated_data.get('received', instance.received) if validated_data.get('received', instance.received) else 0)
        instance.save()
        return instance

class OrderStatusUpdateSerializer(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.IntegerField())

    
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
    capsule_price = serializers.IntegerField()
    client_type = serializers.ChoiceField(choices=models.Client.CLIENT_TYPE)

    order_count = serializers.IntegerField()
    paid = serializers.IntegerField()
    payment_type = serializers.ChoiceField(choices=models.Order.PAYMENT_TYPE)

    def validate_region(self, region):
        try:
            region = models.Region.objects.get(id=region)
        except:
            raise serializers.ValidationError('region not found')
        return region 
    
    def validate_code_number(self, code_number):
        client = models.Client.objects.filter(code_number=code_number).first()
        if client:
            raise serializers.ValidationError('client already exists')
        else:
            return code_number
    

    def create(self, validated_data):
        with transaction.atomic():
            client = models.Client.objects.create(
                full_name=validated_data['full_name'],
                code_number=validated_data['code_number'],
                region=validated_data['region'],
                location_text=validated_data['location_text'],
                cooler=validated_data['cooler'],    
                price=validated_data['capsule_price'],
                client_type=validated_data['client_type'],
                debt=(validated_data['capsule_price'] * validated_data['order_count']) - validated_data['paid']
            )  
            for phone in validated_data['phone_numbers']:
                models.ClientPhoneNumber.objects.create(number=phone, client=client)
            
            order = models.Order.objects.create(
                client=client,
                count=validated_data['order_count'],
                price=validated_data['capsule_price'] * validated_data['order_count'],
                paid=validated_data['paid'],
                the_rest=validated_data['order_count'],
                indebtedness=(validated_data['capsule_price'] * validated_data['order_count']) - validated_data['paid'],
                payment_type=validated_data['payment_type'],
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
            'id', 'count', 'price', 'received', 'the_rest', 'paid', 'indebtedness', 'status', 'payment_type', 'created_at'
        ]



class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'id', 'count', 'price', 'the_rest', 'indebtedness', 'payment_type', 
            'status'
        ]
    


class ClientOrderCreateSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    count = serializers.IntegerField()
    paid = serializers.IntegerField(required=False)
    payment_type = serializers.ChoiceField(choices=models.Order.PAYMENT_TYPE)
    indebtedness = serializers.IntegerField(required=False)

    def validate_client_id(self, client_id):
        try:
            client = models.Client.objects.get(id=client_id)
            order = models.Order.objects.filter(client=client_id).order_by('-created_at').first()
            if order.status != 'delivered':
                raise serializers.ValidationError('previous order not delivered')
        except models.Client.DoesNotExist:
            raise serializers.ValidationError('client not found')
        return client
    
    def create(self, validated_data):
        with transaction.atomic():
            price = validated_data['client_id'].price * validated_data['count']
            order = models.Order.objects.create(
                client=validated_data['client_id'],
                count=validated_data['count'],
                price=price,
                the_rest=validated_data['count'],
                received=0,
                paid=validated_data['paid'],
                indebtedness=validated_data['indebtedness'],
                payment_type=validated_data['payment_type'],
            )
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
            'id', 'code_number', 'full_name', 'region', 'numbers', 'cooler', 'location_text', 'orders_count', 'empty_dish', 'all_debt', 'price', 'client_type'
        ]

    def get_numbers(self, obj):
        numbers = models.ClientPhoneNumber.objects.filter(client=obj)
        return ClientPhoneNumberSerializer(numbers, many=True).data
    
    def get_orders_count(self, obj):
        return models.Order.objects.filter(client=obj).count()
    
    def get_empty_dish(self, obj):
        return models.Order.objects.filter(client=obj).aggregate(
            empty_dish=Sum('the_rest')
        )['empty_dish']
        
    def get_all_debt(self, obj):
        return models.Order.objects.filter(client=obj).aggregate(
            all_debt=Sum('indebtedness')
        )['all_debt']


class ClientListSerializer(serializers.ModelSerializer):
    region = RegionListSerializer()
    numbers = serializers.SerializerMethodField(method_name='get_numbers')
    order = serializers.SerializerMethodField(method_name='get_order')
    number_of_trips = serializers.SerializerMethodField(method_name='get_number_of_trips')

    class Meta:
        model = models.Client
        fields = [
            'id', 'code_number', 'full_name', 'region', 'numbers', 'cooler', 'location_text', 'order', 'client_type', 'number_of_trips',
        ]

    def get_numbers(self, obj):
        numbers = models.ClientPhoneNumber.objects.filter(client=obj)
        return ClientPhoneNumberSerializer(numbers, many=True).data
    
    def get_order(self, obj):
        order =  models.Order.objects.filter(client=obj).last()
        return OrderListSerializer(order).data

    def get_number_of_trips(self, obj):
        number_of_trips = models.NumberOfTrips.objects.filter(client=obj).last()
        if number_of_trips:
            return {"id": number_of_trips.id, "number": number_of_trips.number}
        else:
            return None 
        
class ClientUpdateSerializer(serializers.ModelSerializer):
    numbers = ClientPhoneNumberSerializer(many=True)

    class Meta:
        model = models.Client
        fields = [
            'code_number', 'full_name', 'region', 'numbers', 'cooler', 'location_text', 'client_type', 'price'
        ]


    def update(self, instance, validated_data):
        numbers_data = validated_data.pop('numbers', [])

        instance.code_number = validated_data.get('code_number', instance.code_number)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.region = validated_data.get('region', instance.region)
        instance.cooler = validated_data.get('cooler', instance.cooler)
        instance.location_text = validated_data.get('location_text', instance.location_text)
        instance.client_type = validated_data.get('client_type', instance.client_type)
        instance.price = validated_data.get('price', instance.price)
        models.ClientPhoneNumber.objects.filter(client=instance).delete()
        for number_data in numbers_data:
            models.ClientPhoneNumber.objects.update_or_create(client=instance, number=number_data['number'])
        instance.save()
        return instance
    

class ClientOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'count', 'price', 'the_rest', 'received', 'paid', 'indebtedness', 'status', 'payment_type'
        ]

    def update(self, instance, validated_data):
        instance.count = validated_data.get('count', instance.count)
        instance.price = validated_data.get('price', instance.price)
        instance.received = validated_data.get('received', instance.received)
        instance.paid = validated_data.get('paid', instance.paid)
        instance.status = validated_data.get('status', instance.status)
        instance.the_rest = validated_data.get('count', instance.count) - (validated_data.get('received', instance.received) if validated_data.get('received', instance.received) else 0)
        instance.payment_type = validated_data.get('payment_type', instance.payment_type)
        instance.indebtedness = validated_data.get('indebtedness', instance.indebtedness)
        instance.save()
        return instance


class OrderStatusUpdateSerializer(serializers.Serializer):
    ids = serializers.ListSerializer(child=serializers.IntegerField())


class NumberOfTripsCreateSerializer(serializers.Serializer):
    client_ids = serializers.ListSerializer(child=serializers.IntegerField())
    number = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            for client_id in validated_data['client_ids']:
                try:
                    client = models.Client.objects.get(id=client_id)
                    number_of_trips = models.NumberOfTrips.objects.create(client=client, number=validated_data['number'])
                except models.Client.DoesNotExist:
                    raise serializers.ValidationError('client not found')
            return {"message": "successfully created"}
        
class ClientOrderListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            'received',
        ]
    
    def update(self, instance, validated_data):
        instance.received = validated_data.get('received', instance.received)
        instance.the_rest = instance.count - instance.received
        instance.status = 'delivered'
        instance.save()
        return instance
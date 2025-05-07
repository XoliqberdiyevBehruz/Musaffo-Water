from rest_framework import views, generics, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from common import models, serializers, filters


class ClientCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ClientCreateSerializer
    queryset = models.Client

    def post(self, request):
        serializer = serializers.ClientCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegionListApiView(generics.ListAPIView):
    serializer_class = serializers.RegionListSerializer
    queryset = models.Region.objects.all()


class ClientOrderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ClientOrderCreateSerializer
    queryset = models.Order

    def post(self, request):
        serializer = serializers.ClientOrderCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            res = serializer.save()
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ClientOrderListApiView(generics.GenericAPIView):
    serializer_class = serializers.ClientOrderListSerializer
    queryset = models.Order

    def get(self, request, client_id):
        orders = models.Order.objects.filter(client=client_id).order_by('-created_at')
        serializer = serializers.ClientOrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ClientDetailApiView(generics.GenericAPIView):
    serializer_class = serializers.ClientDetailSerializer
    queryset = models.Client

    def get(self, request, client_id):
        try:
            client = models.Client.objects.get(id=client_id)
        except models.Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ClientDetailSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ClientListApiView(generics.ListAPIView):
    serializer_class = serializers.ClientListSerializer
    queryset = models.Client.objects.order_by('-created_at').distinct()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ClientFilter
    


class ClientUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.ClientUpdateSerializer
    queryset = models.Client

    def patch(self, request, id):
        try:
            client = models.Client.objects.get(id=id)
        except models.Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ClientUpdateSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ClientOrderUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.ClientOrderUpdateSerializer
    queryset = models.Order
    lookup_field = 'id'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderStatusUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderStatusUpdateSerializer
    queryset = models.Order

    def post(self, request):
        serializer = serializers.OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            for id in data['ids']:
                try:
                    order = models.Order.objects.get(id=id)
                    order.status = 'taken'
                    order.save()
                except models.Order.DoesNotExist:
                    return Response({'success': False}, status=status.HTTP_404_NOT_FOUND)
            return Response({'success': True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusChangeApiView(generics.GenericAPIView):
    serializer_class = None 
    queryset = models.Order.objects.all()

    def get(self, request, order_id):
        try:
            order = models.Order.objects.get(id=order_id)
        except models.Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.status = 'cancelled'
        order.save()
        return Response({'status': order.status}, status=status.HTTP_200_OK)


class NumberOfTripsCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.NumberOfTripsCreateSerializer
    queryset = models.NumberOfTrips.objects.all()

    def post(self, request):
        serializer = serializers.NumberOfTripsCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NumberOfTripsDeleteApiView(generics.DestroyAPIView):
    queryset = models.NumberOfTrips.objects.all()
    lookup_field = 'id'


class ClientOrderListUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.ClientOrderListUpdateSerializer
    queryset = models.Order

    def patch(self, request, order_id):
        try:
            order = models.Order.objects.get(id=order_id)
        except models.Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ClientOrderListUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)
from django.urls import path 

from common import views 


urlpatterns = [
    path('client/create/', views.ClientCreateApiView.as_view(), name='client create api'),
    path('region/list/', views.RegionListApiView.as_view(), name='region list api'),
    path('client/order/create/', views.ClientOrderCreateApiView.as_view(), name='client order create api'),
    path('client/<int:client_id>/order/list/', views.ClientOrderListApiView.as_view(), name='client orders list api'),
    path('client/<int:client_id>/', views.ClientDetailApiView.as_view(), name='client detail api'),
    path('client/list/', views.ClientListApiView.as_view(), name='client list api'),
    path('client/<int:id>/update/', views.ClientUpdateApiView.as_view(), name='client update api'),
    path('client/order/<int:id>/update/', views.ClientOrderUpdateApiView.as_view(), name='client order update api'),
    path('order/status/update/', views.OrderStatusUpdateApiView.as_view(), name='order status update api'),
    path('order/<int:order_id>/change/status/', views.OrderStatusChangeApiView.as_view(), name='order status change api'),
]

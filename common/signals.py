from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# from common import models 


# @receiver(post_save, sender=models.Order)
# def update_client_debt(sender, instance, created, **kwargs):
#     if created:
#         client = instance.client
#         if client.debt < 0:
#             client.debt += instance.indebtedness
#             client.save()
    # else:
    #     # If the order is updated, recalculate the debt
    #     total_paid = models.Order.objects.filter(client=client).aggregate(Sum('paid'))['paid__sum'] or 0
    #     total_price = models.Order.objects.filter(client=client).aggregate(Sum('price'))['price__sum'] or 0
    #     client.debt = total_price - total_paid
    #     client.save()
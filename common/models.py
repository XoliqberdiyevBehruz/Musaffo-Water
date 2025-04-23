from django.db import models 

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True 


class Region(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Client(BaseModel):
    code_number = models.PositiveIntegerField(unique=True)
    full_name = models.CharField(max_length=250)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='clients')
    location_text = models.CharField(max_length=250)
    debt = models.PositiveIntegerField(default=0)
    cooler = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class ClientPhoneNumber(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='numbers')
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number


class Order(BaseModel):
    STATUS = (
        ('yangi', 'yangi'),
        ('berilgan', 'berilgan'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    count = models.PositiveSmallIntegerField()
    price = models.PositiveBigIntegerField()
    the_rest = models.PositiveIntegerField(null=True, blank=True)
    received = models.PositiveIntegerField(null=True, blank=True)
    paid = models.PositiveBigIntegerField(null=True, blank=True)
    indebtedness = models.PositiveBigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS, default='yangi')

    def __str__(self):
        return f'{self.client} - {self.count} - {self.price}'



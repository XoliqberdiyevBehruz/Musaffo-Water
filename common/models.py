from django.db import models 

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True 


class Region(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return "{} - {}".format(self.name, self.number_of_trips)


class Client(BaseModel):
    CLIENT_TYPE = (
        ("physical_person", "physical_person"),
        ("legal_person", "legal_person"),
    )

    code_number = models.PositiveIntegerField(unique=True)
    full_name = models.CharField(max_length=250)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='clients')
    location_text = models.CharField(max_length=250)
    debt = models.BigIntegerField(default=0)
    cooler = models.CharField(max_length=50)
    price = models.PositiveBigIntegerField()
    client_type = models.CharField(max_length=50, choices=CLIENT_TYPE)

    def __str__(self):
        return self.full_name


class ClientPhoneNumber(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='numbers')
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number


class Order(BaseModel):
    STATUS = (
        ('new', 'new'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled')
    )
    PAYMENT_TYPE = (
        ("card", "card"),
        ("cash", "cash"),
        ("account_number", "account_number"),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    count = models.PositiveSmallIntegerField()
    price = models.PositiveBigIntegerField()
    the_rest = models.PositiveIntegerField(null=True, blank=True)
    received = models.PositiveIntegerField(null=True, blank=True)
    paid = models.PositiveBigIntegerField(null=True, blank=True)
    indebtedness = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='new')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE)

    def __str__(self):
        return f'{self.client} - {self.count} - {self.price}'


class NumberOfTrips(BaseModel):
    number = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='number_of_trips')

    def __str__(self):
        return "{} - {}".format(self.client, self.number)
    
    
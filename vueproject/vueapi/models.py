from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length = 50)
    file = models.FileField(upload_to='upload/%Y/%m/%d')
    size = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name

class Content(models.Model):
    Product_category = models.CharField(max_length=20)
    Product_name = models.CharField(max_length=50)
    Address = models.CharField(max_length=128)
    Customer_name = models.CharField(max_length=128)
    Development_unit = models.CharField(max_length=128)
    Customer_manager = models.CharField(max_length=50)
    Opening_status = models.CharField(max_length=50)
    Order_time = models.DateField()
    # Order_time = models.FloatField()
    Completion_time = models.DateField(null=True)
    # Completion_time = models.FloatField(null=True)
    Quantity_ordered = models.IntegerField()

    def __unicode__(self):
        return self.Address

class User(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.username

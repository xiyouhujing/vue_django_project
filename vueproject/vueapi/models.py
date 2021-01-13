from django.db import models

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='upload/%Y/%m/%d')
    size = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Content(models.Model):
    id = models.AutoField(primary_key=True)
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

class Monitor(models.Model):
    id = models.AutoField(primary_key=True)
    Region = models.CharField(max_length=20)
    Monitor_points = models.CharField(max_length=128)
    Longitude = models.DecimalField(max_digits=15,decimal_places=12)
    Latitude = models.DecimalField(max_digits=15,decimal_places=12)

    def __unicode__(self):
        return self.Monitor_points

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __unicode__(self):
        return self.username

class Picture(models.Model):
    pic_name = models.CharField(max_length=50)
    pic_size = models.CharField(max_length=50,null=True)
    pic_path = models.ImageField(upload_to='pic_folder/', default='pic_folder/None/no_image.pig')

    def __unicode__(self):
        return self.pic_name
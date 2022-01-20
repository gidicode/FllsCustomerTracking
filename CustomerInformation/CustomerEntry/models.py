from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')

# Create your models here.
class Riders(models.Model):
    rider_name = models.CharField(max_length=50, null=True)
    rider_Number = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.rider_name}"


class Riders_Log(models.Model):
    customer_name = models.CharField(max_length=50, null=True)
    customer_contact = models.CharField(validators=[phone_regex], max_length=11, null=True, unique=True )
    Rider = models.ForeignKey(Riders, null=True, on_delete= models.SET_NULL)
    discount_amount = models.DecimalField(max_digits=10, blank=True, default=0.00, decimal_places=2)
    count = models.ManyToManyField('MultipleEntries', blank=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)    

    def __str__(self):
        return f"{self.customer_name, self.customer_contact}"

    class Meta:
        ordering = ('-date_created',)

class MultipleEntries(models.Model):
    customer = models.ForeignKey(Riders_Log, on_delete=models.SET_NULL, null=True)
    customer_contact = models.CharField(validators=[phone_regex], max_length=11, null=True)
    Rider = models.ForeignKey(Riders, null=True, on_delete= models.SET_NULL)
    discount_amount = models.DecimalField(max_digits=10, blank=True, default=0.00, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"{self.customer}" f"{  self.customer_contact}" + " " f"{self.date_created}"
    
    class Meta:
        ordering = ('-date_created',)
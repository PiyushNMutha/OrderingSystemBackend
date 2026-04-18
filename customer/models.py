from django.db import models
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'customer'
        managed = False

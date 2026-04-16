from django.db import models

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    table_id = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        managed = False
from django.db import models
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    item_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_item'
        managed = False

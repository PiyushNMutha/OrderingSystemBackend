from django.db import models

class MenuCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'menu_category'
        managed = False

    def __str__(self):
        return self.category_name

class MenuItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    category_id = models.IntegerField()
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    class Meta:
        db_table = 'menu_item'
        managed = False

    def __str__(self):
        return self.item_name

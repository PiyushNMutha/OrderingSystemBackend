from django.db import models

class CafeteriaTable(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=15, default='Free')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cafeteria_table'   # VERY IMPORTANT
        managed = False                # Django will NOT create table

    def __str__(self):
        return f"Table {self.table_number} - {self.status}"

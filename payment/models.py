class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    payment_mode = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20, default='Pending')

    class Meta:
        db_table = 'payment'
        managed = False
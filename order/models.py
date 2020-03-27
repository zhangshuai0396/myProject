# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Order(models.Model):
    u_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'order'


class Orderaddress(models.Model):
    order_address = models.CharField(max_length=255)
    order_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orderaddress'


class Goodorder(models.Model):
    good_id = models.IntegerField()
    order_id = models.IntegerField()
    buy_good_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goodorder'

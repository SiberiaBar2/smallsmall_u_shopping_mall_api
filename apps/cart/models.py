from django.db import models

# 相当于创建表
# Create your models here.
class Cart(models.Model):
    id = models.AutoField(primary_key=True,null=False, unique=True)
    email = models.CharField(null=False,max_length=255, unique=True)
    sku_id = models.CharField(null=False,max_length=255, unique=True)
    nums = models.IntegerField()
    is_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shopping_cart'
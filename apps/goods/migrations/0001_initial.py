# Generated by Django 5.1.4 on 2025-01-06 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('sku_id', models.CharField(blank=True, max_length=255, null=True)),
                ('target_url', models.CharField(blank=True, max_length=255, null=True)),
                ('jd_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('p_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('shop_name', models.CharField(blank=True, max_length=255, null=True)),
                ('shop_id', models.IntegerField(blank=True, null=True)),
                ('spu_id', models.CharField(blank=True, max_length=255, null=True)),
                ('mk_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('vender_id', models.IntegerField(blank=True, null=True)),
                ('find', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'goods',
                'managed': False,
            },
        ),
    ]

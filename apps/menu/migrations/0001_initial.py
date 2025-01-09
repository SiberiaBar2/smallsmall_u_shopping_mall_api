# Generated by Django 5.1.4 on 2025-01-06 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_menu_id', models.IntegerField()),
                ('main_menu_name', models.CharField(max_length=255)),
                ('main_menu_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'main_menu',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_menu_id', models.IntegerField(blank=True, null=True)),
                ('sub_menu_id', models.IntegerField(blank=True, null=True)),
                ('sub_menu_type', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_menu_name', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_menu_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'sub_menu',
                'managed': False,
            },
        ),
    ]

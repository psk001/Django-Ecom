# Generated by Django 4.0.4 on 2022-05-14 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_customer_store_custo_last_na_e6a359_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='customer',
            name='store_custo_last_na_e6a359_idx',
        ),
        migrations.AlterModelTable(
            name='customer',
            table=None,
        ),
    ]

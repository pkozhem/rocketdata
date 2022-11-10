# Generated by Django 4.1.3 on 2022-11-10 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, related_name='entity', to='products.product'),
        ),
    ]
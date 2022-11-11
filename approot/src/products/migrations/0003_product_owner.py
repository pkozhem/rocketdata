# Generated by Django 4.1.3 on 2022-11-11 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
        ('products', '0002_alter_product_date_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_owner', to='entities.entity'),
        ),
    ]
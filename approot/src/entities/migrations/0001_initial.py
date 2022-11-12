# Generated by Django 4.1.3 on 2022-11-12 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Factory'), (1, 'Distributor'), (2, 'Dealership'), (3, 'Retail network'), (4, 'Entrepreneur')], default=0, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True, unique=True)),
                ('debt', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(blank=True, default=None, related_name='entity', to='products.product')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent', to='entities.entity')),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=256, null=True, unique=True)),
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='entities.entity')),
            ],
            options={
                'verbose_name': 'Contacts',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, default='Belarus', max_length=56, null=True)),
                ('city', models.CharField(blank=True, default='Minsk', max_length=85, null=True)),
                ('street', models.CharField(blank=True, default='Victory', max_length=60, null=True)),
                ('house', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('contacts', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='entities.contacts')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]

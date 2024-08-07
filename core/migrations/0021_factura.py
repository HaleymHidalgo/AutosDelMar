# Generated by Django 5.0.6 on 2024-07-03 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_ordencompra_detalleorden'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_emision', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.ordencompra')),
            ],
        ),
    ]

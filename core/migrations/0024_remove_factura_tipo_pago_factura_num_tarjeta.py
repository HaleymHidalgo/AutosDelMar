# Generated by Django 5.0.6 on 2024-07-12 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_factura_tipo_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='tipo_pago',
        ),
        migrations.AddField(
            model_name='factura',
            name='num_tarjeta',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

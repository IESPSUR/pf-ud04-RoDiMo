# Generated by Django 4.1.2 on 2022-10-31 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0005_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('importe', models.FloatField()),
                ('unidades', models.IntegerField()),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Nombre', to='tienda.producto')),
            ],
        ),
    ]

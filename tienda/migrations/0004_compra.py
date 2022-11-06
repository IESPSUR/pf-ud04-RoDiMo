# Generated by Django 4.1.2 on 2022-11-06 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('importe', models.FloatField()),
                ('unidades', models.IntegerField()),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Nombre', to='tienda.producto', to_field='nombre')),
            ],
        ),
    ]
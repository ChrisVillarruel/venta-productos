# Generated by Django 3.0.2 on 2020-08-18 21:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0005_auto_20200816_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('supername', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('dni', models.CharField(max_length=10, unique=True, verbose_name='DNI')),
                ('birthday', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Nacimiento')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Direccion')),
                ('sexo', models.CharField(default='name', max_length=10, verbose_name='Genero')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'Cliente',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Producto Vendido',
                'verbose_name_plural': 'Productos Vendidos',
                'db_table': 'DeSale',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre del Producto')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d')),
                ('pvp', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'Producto',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cli', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employe.Client')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'db_table': 'Venta',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=1, max_length=100, unique=True, verbose_name='Nombre de la Categoria'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Employe',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.AddField(
            model_name='product',
            name='cate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employe.Category'),
        ),
        migrations.AddField(
            model_name='detsale',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employe.Product'),
        ),
        migrations.AddField(
            model_name='detsale',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employe.Sale'),
        ),
    ]

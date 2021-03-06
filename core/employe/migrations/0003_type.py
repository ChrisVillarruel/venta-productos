# Generated by Django 3.0.2 on 2020-08-10 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employe', '0002_employe_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(max_length=100, verbose_name='Tipo de Empleado')),
            ],
            options={
                'verbose_name': 'Tipo de Empleado',
                'verbose_name_plural': 'Tipos de Empleados',
                'db_table': 'Tipo',
                'ordering': ['id'],
            },
        ),
    ]

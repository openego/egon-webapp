# Generated manually with Django 3.2.18 on 2023-04-18 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_demandheatinghhcts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demandcts',
            name='demandmodel_ptr',
        ),
        migrations.RemoveField(
            model_name='demandheatinghhcts',
            name='demandmodel_ptr',
        ),
        migrations.RemoveField(
            model_name='demandhousehold',
            name='demandmodel_ptr',
        ),
        migrations.DeleteModel(
            name='DemandCts',
        ),
        migrations.DeleteModel(
            name='DemandHousehold',
        ),
        migrations.DeleteModel(
            name='DemandHeatingHhCts',
        ),
        migrations.DeleteModel(
            name='DemandModel',
        ),
    ]

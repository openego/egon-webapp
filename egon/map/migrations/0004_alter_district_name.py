# Generated by Django 3.2.3 on 2021-09-08 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_alter_mvgriddistricts_geom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]

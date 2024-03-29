# Generated by Django 3.2.18 on 2023-05-22 12:40

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0026_ch4voronoi'),
    ]

    operations = [
        migrations.CreateModel(
            name='H2Voronoi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('scn_name', models.CharField(max_length=64)),
            ],
        ),
    ]

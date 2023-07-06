# Generated by Django 3.2.18 on 2023-06-29 11:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0046_rename_supply_pv_roof_top_potential_electricity_production_100re_feedin_mvgriddistrictdata100re_supp'),
    ]

    operations = [
        migrations.CreateModel(
            name='CH4Voronoi100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('scn_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='EHVHVSubstation100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EHVLine100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlexPotElDynamicLineRating100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
                ('dlr', models.PositiveIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('vector_tiles', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='H2Voronoi100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('scn_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='HVLine100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HVMVSubstation100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MethaneGridLine100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PotentialCH4Stores100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('e_nom', models.FloatField(null=True, verbose_name='Storage Capacity (MWh)')),
            ],
        ),
        migrations.CreateModel(
            name='PotentialH2UndergroundStorage100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('e_nom_max', models.FloatField(null=True, verbose_name='Storage Capacity (MWh)')),
            ],
        ),
    ]
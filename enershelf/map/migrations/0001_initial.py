# Generated by Django 3.2.3 on 2021-05-27 15:33

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('name', models.CharField(max_length=50)),
                ('area', models.FloatField()),
                ('population', models.BigIntegerField()),
                ('hospitals', models.IntegerField()),
                ('den_p_h_km', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layer_type', models.CharField(choices=[('country', 'Land'), ('state', 'Bundesland'), ('district', 'Kreis'), ('municipality', 'Gemeinde')], max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('type', models.CharField(max_length=40)),
                ('nuts', models.CharField(max_length=5)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='map.region')),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ags', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=60)),
                ('type', models.CharField(max_length=40)),
                ('nuts', models.CharField(max_length=5)),
                ('district_id', models.BigIntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='map.region')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('type', models.CharField(max_length=40)),
                ('nuts', models.CharField(max_length=5)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='map.region')),
            ],
        ),
    ]

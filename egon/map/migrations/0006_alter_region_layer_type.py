# Generated by Django 3.2.18 on 2023-04-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_alter_municipality_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='layer_type',
            field=models.CharField(choices=[('country', 'Country'), ('state', 'State'), ('district', 'District'), ('municipality', 'Municipality')], max_length=12),
        ),
    ]
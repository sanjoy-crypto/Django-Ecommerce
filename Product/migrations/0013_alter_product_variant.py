# Generated by Django 3.2.2 on 2021-06-05 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_auto_20210605_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='variant',
            field=models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Model', 'Model'), ('Size-Color', 'Size-Color')], default='None', max_length=10),
        ),
    ]

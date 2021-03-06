# Generated by Django 2.2.7 on 2019-11-30 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vegan_spider_app', '0005_auto_20191130_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vegan_spider_app.Unit'),
        ),
    ]

# Generated by Django 2.2.7 on 2019-11-29 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vegan_spider_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('photo', models.ImageField(blank=True, upload_to='ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('photo', models.ImageField(blank=True, upload_to='recipes')),
                ('desc', models.CharField(max_length=512)),
                ('link', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('short_name', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='UserIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vegan_spider_app.Ingredient')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vegan_spider_app.Unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vegan_spider_app.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vegan_spider_app.Recipe')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vegan_spider_app.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='vegan_spider_app.RecipeIngredient', to='vegan_spider_app.Ingredient'),
        ),
        migrations.AddField(
            model_name='user',
            name='ingredients',
            field=models.ManyToManyField(through='vegan_spider_app.UserIngredient', to='vegan_spider_app.Ingredient'),
        ),
    ]

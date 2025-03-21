# Generated by Django 5.1.7 on 2025-03-07 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('brief_description', models.TextField()),
                ('image1', models.ImageField(upload_to='articles/images/')),
                ('image2', models.ImageField(upload_to='articles/images/')),
                ('image3', models.ImageField(upload_to='articles/images/')),
                ('paragraph1', models.TextField()),
                ('paragraph2', models.TextField()),
                ('paragraph3', models.TextField()),
                ('paragraph4', models.TextField()),
                ('paragraph5', models.TextField()),
                ('paragraph6', models.TextField()),
                ('paragraph7', models.TextField()),
                ('paragraph8', models.TextField()),
                ('paragraph9', models.TextField()),
                ('paragraph10', models.TextField()),
            ],
        ),
    ]

# Generated by Django 2.2 on 2019-05-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_restaurant_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
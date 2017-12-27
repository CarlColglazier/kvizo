# Generated by Django 2.0 on 2017-12-25 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20171225_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='difficulty',
            field=models.CharField(choices=[('MS', 'Middle School'), ('HS', 'High School'), ('College', 'College'), ('Open', 'Open'), (None, 'None')], max_length=7),
        ),
        migrations.AlterField(
            model_name='tossup',
            name='difficulty',
            field=models.CharField(choices=[('MS', 'Middle School'), ('HS', 'High School'), ('College', 'College'), ('Open', 'Open'), (None, 'None')], max_length=7),
        ),
    ]
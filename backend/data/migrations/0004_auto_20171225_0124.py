# Generated by Django 2.0 on 2017-12-25 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20171224_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='category',
            field=models.CharField(choices=[('Literature', (('LA', 'American Literature'), ('LB', 'British Literature'), ('LE', 'European Literature'), ('LW', 'World Literature'), ('LC', 'Classical Literature'), ('LO', 'Other Literature'))), ('History', (('LA', 'American History'), ('LB', 'British History'), ('LE', 'European History'), ('LW', 'World History'), ('LC', 'Classical History'), ('LO', 'Other History'))), ('Science', (('SB', 'Biology'), ('SC', 'Chemistry'), ('SM', 'Math'), ('CS', 'Computer Science'), ('SO', 'Science'))), ('Fine Arts', (('FA', 'Auditory Fine Arts'), ('FV', 'Visual Fine Arts'), ('AV', 'Audiovisual Fine Arts'), ('FO', 'Other Fine Arts'))), ('Other', (('RL', 'Religion'), ('MY', 'Mythology'), ('SS', 'Social Science'), ('GE', 'Geography'), ('CE', 'Current Events'), ('TR', 'Trash'), (None, 'None')))], max_length=2),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='difficulty',
            field=models.CharField(choices=[('M', 'Middle School'), ('H', 'High School'), ('C', 'College'), ('O', 'Open'), (None, 'None')], max_length=1),
        ),
        migrations.AlterField(
            model_name='tossup',
            name='category',
            field=models.CharField(choices=[('Literature', (('LA', 'American Literature'), ('LB', 'British Literature'), ('LE', 'European Literature'), ('LW', 'World Literature'), ('LC', 'Classical Literature'), ('LO', 'Other Literature'))), ('History', (('LA', 'American History'), ('LB', 'British History'), ('LE', 'European History'), ('LW', 'World History'), ('LC', 'Classical History'), ('LO', 'Other History'))), ('Science', (('SB', 'Biology'), ('SC', 'Chemistry'), ('SM', 'Math'), ('CS', 'Computer Science'), ('SO', 'Science'))), ('Fine Arts', (('FA', 'Auditory Fine Arts'), ('FV', 'Visual Fine Arts'), ('AV', 'Audiovisual Fine Arts'), ('FO', 'Other Fine Arts'))), ('Other', (('RL', 'Religion'), ('MY', 'Mythology'), ('SS', 'Social Science'), ('GE', 'Geography'), ('CE', 'Current Events'), ('TR', 'Trash'), (None, 'None')))], max_length=2),
        ),
        migrations.AlterField(
            model_name='tossup',
            name='difficulty',
            field=models.CharField(choices=[('M', 'Middle School'), ('H', 'High School'), ('C', 'College'), ('O', 'Open'), (None, 'None')], max_length=1),
        ),
    ]

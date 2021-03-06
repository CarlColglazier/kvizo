# Generated by Django 2.0 on 2017-12-24 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_bonus_tossup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='category',
            field=models.CharField(choices=[('Literature', (('LA', 'American Literature'), ('LB', 'British Literature'), ('LE', 'European Literature'), ('LW', 'World Literature'), ('LC', 'Classical Literature'), ('LO', 'Other Literature'))), ('History', (('LA', 'American History'), ('LB', 'British History'), ('LE', 'European History'), ('LW', 'World History'), ('LC', 'Classical History'), ('LO', 'Other History'))), ('Science', (('SB', 'Biology'), ('SC', 'Chemistry'), ('SM', 'Math'), ('CS', 'Computer Science'), ('SO', 'Other Science'))), ('Fine Arts', (('FA', 'Auditory Fine Arts'), ('FV', 'Visual Fine Arts'), ('AV', 'Audiovisual Fine Arts'), ('FO', 'Other Fine Arts'))), ('Other', (('RL', 'Religion'), ('MY', 'Mythology'), ('SS', 'Social Science'), ('GE', 'Geography'), ('CE', 'Current Events'), ('TR', 'Trash'), ('', 'None')))], max_length=2),
        ),
        migrations.AlterField(
            model_name='bonus',
            name='difficulty',
            field=models.CharField(choices=[('M', 'Middle School'), ('H', 'High School'), ('C', 'College'), ('O', 'Open'), ('', 'None')], max_length=1),
        ),
        migrations.AlterField(
            model_name='tossup',
            name='category',
            field=models.CharField(choices=[('Literature', (('LA', 'American Literature'), ('LB', 'British Literature'), ('LE', 'European Literature'), ('LW', 'World Literature'), ('LC', 'Classical Literature'), ('LO', 'Other Literature'))), ('History', (('LA', 'American History'), ('LB', 'British History'), ('LE', 'European History'), ('LW', 'World History'), ('LC', 'Classical History'), ('LO', 'Other History'))), ('Science', (('SB', 'Biology'), ('SC', 'Chemistry'), ('SM', 'Math'), ('CS', 'Computer Science'), ('SO', 'Other Science'))), ('Fine Arts', (('FA', 'Auditory Fine Arts'), ('FV', 'Visual Fine Arts'), ('AV', 'Audiovisual Fine Arts'), ('FO', 'Other Fine Arts'))), ('Other', (('RL', 'Religion'), ('MY', 'Mythology'), ('SS', 'Social Science'), ('GE', 'Geography'), ('CE', 'Current Events'), ('TR', 'Trash'), ('', 'None')))], max_length=2),
        ),
        migrations.AlterField(
            model_name='tossup',
            name='difficulty',
            field=models.CharField(choices=[('M', 'Middle School'), ('H', 'High School'), ('C', 'College'), ('O', 'Open'), ('', 'None')], max_length=1),
        ),
    ]

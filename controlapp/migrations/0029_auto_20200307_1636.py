# Generated by Django 3.0 on 2020-03-07 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controlapp', '0028_optionunit_voterunit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventunit',
            old_name='eventVote',
            new_name='eventSelection',
        ),
    ]

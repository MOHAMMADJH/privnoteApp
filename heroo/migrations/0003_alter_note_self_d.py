# Generated by Django 4.0.4 on 2022-05-13 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroo', '0002_remove_note_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='self_d',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]

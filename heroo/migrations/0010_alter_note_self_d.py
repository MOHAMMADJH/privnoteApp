# Generated by Django 3.2.13 on 2022-05-17 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroo', '0009_alter_note_date_c'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='self_d',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
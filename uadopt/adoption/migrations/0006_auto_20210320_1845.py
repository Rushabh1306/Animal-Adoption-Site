# Generated by Django 3.1.5 on 2021-03-20 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adoption', '0005_auto_20210320_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='type',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
    ]
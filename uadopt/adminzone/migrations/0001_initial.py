# Generated by Django 3.1.5 on 2021-04-02 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('org_name', models.CharField(max_length=50, null=True)),
                ('org_address', models.TextField(null=True)),
                ('org_city', models.CharField(max_length=50, null=True)),
                ('org_state', models.CharField(max_length=50, null=True)),
                ('org_location', models.CharField(max_length=50, null=True)),
                ('org_report', models.CharField(max_length=50, null=True)),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

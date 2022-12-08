# Generated by Django 2.1.15 on 2022-12-08 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_auto_20221209_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='consultant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultant_request', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='request',
            name='faction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='faction_request', to='users.Faction'),
        ),
    ]

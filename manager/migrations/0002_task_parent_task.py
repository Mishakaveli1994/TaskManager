# Generated by Django 4.0.4 on 2022-04-18 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='parent_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.task'),
        ),
    ]

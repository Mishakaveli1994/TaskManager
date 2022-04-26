# Generated by Django 4.0.4 on 2022-04-26 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_alter_task_assignee_alter_task_tracked_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='resolved',
            field=models.CharField(choices=[('unresolved', 'Unresolved'), ('resolved', 'Resolved')], default='unresolved', max_length=10),
        ),
    ]

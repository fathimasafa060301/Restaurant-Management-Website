# Generated by Django 5.0.2 on 2024-04-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD_APP', '0011_alter_order_status_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.IntegerField(choices=[(0, 'Cancelled'), (1, 'New'), (2, 'Pending'), (3, 'Delivered')], default=1),
        ),
    ]

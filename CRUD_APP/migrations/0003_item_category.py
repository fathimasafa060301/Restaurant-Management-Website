# Generated by Django 5.0.2 on 2024-03-12 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD_APP', '0002_item_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

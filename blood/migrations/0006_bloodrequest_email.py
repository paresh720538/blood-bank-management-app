# Generated by Django 5.0.4 on 2024-04-09 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0005_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]

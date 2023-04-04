# Generated by Django 4.1.7 on 2023-03-28 08:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_alter_post_categorytype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.2.19 on 2023-06-13 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0008_auto_20230612_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]

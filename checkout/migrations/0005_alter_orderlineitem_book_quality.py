# Generated by Django 3.2.19 on 2023-06-28 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_quality'),
        ('checkout', '0004_order_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='book_quality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.quality'),
        ),
    ]

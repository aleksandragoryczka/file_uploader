# Generated by Django 4.2.5 on 2023-09-17 12:45

from django.db import migrations, models
import images.models
import images.validators


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_alter_expiringlink_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='expiration_time_sec',
            field=models.IntegerField(validators=[images.validators.validate_expiration_time_sec]),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=None, upload_to=images.models.upload_to, validators=[images.validators.validate_image_format]),
        ),
    ]

# Generated by Django 3.2.4 on 2021-06-21 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('happyhourscourapi', '0003_auto_20210620_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='happyhourscourapi.location'),
        ),
    ]

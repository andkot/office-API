# Generated by Django 3.1.2 on 2020-10-12 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('officerooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinghistory',
            name='room',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='officerooms.room'),
        ),
        migrations.AddField(
            model_name='bookinghistory',
            name='room_place',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='officerooms.userplace'),
        ),
        migrations.AlterField(
            model_name='bookinghistory',
            name='from_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
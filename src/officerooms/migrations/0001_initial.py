# Generated by Django 3.1.2 on 2020-10-12 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('from_date', models.DateTimeField(auto_now_add=True)),
                ('to_date', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='officerooms.bookinghistory')),
                ('is_booked', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='officerooms.room')),
            ],
        ),
    ]

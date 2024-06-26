# Generated by Django 4.2.13 on 2024-06-03 09:14

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
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ImageField(upload_to='stories/')),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userStories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

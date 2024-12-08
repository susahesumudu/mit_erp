# Generated by Django 5.1.3 on 2024-12-03 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('duration_months', models.IntegerField(help_text='Duration of the course in months')),
                ('theory_hours', models.IntegerField(help_text='Total theory hours for the course')),
                ('practical_hours', models.IntegerField(help_text='Total practical hours for the course')),
                ('fee', models.DecimalField(decimal_places=2, help_text='Total course fee', max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('theory_hours', models.IntegerField(help_text='Theory hours for this module')),
                ('practical_hours', models.IntegerField(help_text='Practical hours for this module')),
                ('fee', models.DecimalField(decimal_places=2, help_text='Fee for this module', max_digits=10)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('theory_hours', models.IntegerField(help_text='Theory hours for this task')),
                ('practical_hours', models.IntegerField(help_text='Practical hours for this task')),
                ('fee', models.DecimalField(decimal_places=2, help_text='Fee for this task', max_digits=10)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='courses.module')),
            ],
        ),
    ]
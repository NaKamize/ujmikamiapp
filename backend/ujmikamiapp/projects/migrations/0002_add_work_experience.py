import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('period', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField()),
                ('current', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower = first / most recent)')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='WorkExperienceTechnology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('experience', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='technologies',
                    to='projects.workexperience',
                )),
            ],
        ),
    ]

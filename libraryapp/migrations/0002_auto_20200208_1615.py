# Generated by Django 3.0.3 on 2020-02-08 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'book', 'verbose_name_plural': 'books'},
        ),
        migrations.AlterModelOptions(
            name='library',
            options={'verbose_name': 'library', 'verbose_name_plural': 'libraries'},
        ),
        migrations.AddField(
            model_name='book',
            name='librarian',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='libraryapp.Librarian'),
            preserve_default=False,
        ),
    ]

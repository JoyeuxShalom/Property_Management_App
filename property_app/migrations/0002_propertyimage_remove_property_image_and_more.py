# Generated by Django 4.2.17 on 2024-12-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property_images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='property',
            name='image',
        ),
        migrations.AddField(
            model_name='property',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='bathrooms',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='property',
            name='bedrooms',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='property',
            name='images',
            field=models.ManyToManyField(related_name='properties', to='property_app.propertyimage'),
        ),
    ]
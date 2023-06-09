# Generated by Django 4.1.7 on 2023-05-07 10:36

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0006_rating_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('subject', models.CharField(max_length=255)),
                ('description', ckeditor.fields.RichTextField()),
                ('content', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='foods/%Y/%m/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='foods.category')),
                ('tags', models.ManyToManyField(to='foods.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='comment',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.foods'),
        ),
        migrations.AlterField(
            model_name='like',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.foods'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.foods'),
        ),
        migrations.DeleteModel(
            name='Food',
        ),
    ]

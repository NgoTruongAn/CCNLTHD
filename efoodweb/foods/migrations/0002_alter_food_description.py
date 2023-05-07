import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]

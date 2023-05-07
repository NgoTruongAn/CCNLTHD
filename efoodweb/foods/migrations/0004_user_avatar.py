from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0003_tag_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to='users/%Y/%m/'),
        ),
    ]
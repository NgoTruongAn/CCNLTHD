from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/%Y/%m/', null=True)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Foods(BaseModel):
    subject = models.CharField(max_length=255)
    description = RichTextField()
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='foods/%Y/%m/', null=True, blank=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.subject


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    content = models.CharField(max_length=255)
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class ActionBase(BaseModel):
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ('food', 'user')


class Like(ActionBase):
    liked = models.BooleanField(default=True)


class Rating(ActionBase):
    rate = models.SmallIntegerField(default=0)
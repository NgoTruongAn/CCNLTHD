from django.contrib import admin
from .models import Category, Foods, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe


class FoodForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Foods
        fields = '__all__'


class TagInlindAdmin(admin.StackedInline):
    model = Foods.tags.through


class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'category']
    search_fields = ['subject', 'description']
    list_filter = ['id', 'subject', 'created_date']
    form = FoodForm
    readonly_fields = ['avatar']
    inlines = [TagInlindAdmin, ]

    def avatar(self, food):
        return mark_safe("<img src='/static/{}' width='120' />".format(food.image.name))


# Register your models here.
admin.site.register(Category)
admin.site.register(Foods, FoodAdmin)
admin.site.register(Tag)


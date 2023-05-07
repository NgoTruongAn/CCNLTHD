from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('foods', views.FoodViewSet)
router.register('users', views.UserViewSet)
router.register('comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

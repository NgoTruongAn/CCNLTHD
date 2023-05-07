from rest_framework import viewsets, generics, parsers, permissions, status
from .models import (
    Category, Foods,
    User, Comment, Tag, Like, Rating
)
from .serializers import (
    CategorySerializer, FoodSerializer,
    UserSerializer, CommentSerializer
)
from .paginators import FoodPaginator
from rest_framework.decorators import action
from rest_framework.views import Response
from .perms import CommentOwner


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FoodViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Foods.objects.filter(active=True)
    serializer_class = FoodSerializer
    pagination_class = FoodPaginator

    def filter_queryset(self, queryset):
        kw = self.request.query_params.get('kw')
        if self.action.__eq__('list') and kw:
            queryset = queryset.filter(subject__icontains=kw)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset

    @action(methods=['get'], detail=True, url_path='foods')
    def foods(self, request, pk):
        c = self.get_object()
        foods = c.food_set.filter(active=True)

        kw = request.query_params.get('kw')
        if kw:
            foods = foods.filter(subject__icontains=kw)

        return Response(FoodSerializer(foods, many=True).data)

    def get_permissions(self):
        if self.action in ['comments', 'like']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='tags')
    def assign_tags(self, request, pk):
        food = self.get_object()
        tags = request.data['tags']
        for t in tags:
            tag, _ = Tag.objects.get_or_create(name=t)
            food.tags.add(tag)
        food.save()

        return Response(FoodSerializer(food, context={'request': request}).data)

    @action(methods=['post'], detail=True, url_path='comments')
    def comments(self, request, pk):
        food = self.get_object()
        c = Comment(content=request.data['content'], food=food, user=request.user)
        c.save()

        return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='like')
    def like(self, request, pk):
        food = self.get_object()
        l, created = Like.objects.get_or_create(food=food, user=request.user)
        if not created:
            l.liked = not l.liked
        l.save()

        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rating')
    def rate(self, request, pk):
        food = self.get_object()
        r, _ = Rating.objects.get_or_create(food=food, user=request.user)
        r.rate = request.data['rate']
        r.save()

        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user', 'update', 'partial_update']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [CommentOwner()]

        return [permissions.AllowAny()]

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import permissions

from .models import News, Comment
from .serializers import NewsSerializer, StatusNewsSerializer, CommentSerializer
from .permisiions import NewsPermission


class PostPagePagination(PageNumberPagination):
    page_size = 3


class NewsViewSet(viewsets.ModelViewSet):
    """
    API для создания, получения, изменения и удаления новостей
    зарегистрированным пользователям is_staff
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [NewsPermission, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', ]
    ordering_fields = ['updated_at', 'created_at']
    pagination_class = PostPagePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    @action(methods=['POST', 'GET'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def leave_status(self, request, pk=None):
        serializer = StatusNewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user.author,
                news=self.get_object()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [NewsPermission, ]

    """
    API для создания и получения комментариев
    """

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )


class CommentUpdate(generics.RetrieveUpdateDestroyAPIView):

    """
    надо доделать срок неделя
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [NewsPermission, ]

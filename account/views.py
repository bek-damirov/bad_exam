from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from .serializers import AuthorRegisterSerializer
from .models import Author, User


class AuthorRegisterAPIView(viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer

    def create_profile(self, request, is_staff):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(is_staff=is_staff)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def author(self, request, pk=None):
        return self.create_profile(request, True)

    @action(methods=['POST'], detail=False)
    def guest(self, request, pk=None):
        return self.create_profile(request, False)

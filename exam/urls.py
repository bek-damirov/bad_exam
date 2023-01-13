"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from account import views as acc_view
from news import views as news_view


schema_view = get_schema_view(
   openapi.Info(
      title="EXAM API",
      default_version='v-0.0.0001',
      description="API для новостей",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="bek@gmail.com"),
      license=openapi.License(name="No Licence"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

acc_router = DefaultRouter()
acc_router.register('register', acc_view.AuthorRegisterAPIView)

news_router = DefaultRouter()
news_router.register('news', news_view.NewsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token),

    path('api/news/', include(news_router.urls)),
    path('api/news/news/<int:news_id>/comment/', news_view.CommentListCreateAPIView.as_view()),
    path('api/comment/<int:comment_id>/', news_view.CommentUpdate.as_view()),

    path('api/accounts/', include(acc_router.urls)),

    # documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),

]

"""kwizzed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from django.urls import re_path
from rest_framework import routers
from kwizzedapi.views import register_user, login_user, QuestionView, AnswerView, CategoryView, PlayerResponseView, ReviewView, PlayerView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Kwizzed API",
        default_version='v1',
        description="API for playing Kwizzed, a trivia game.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="herbisonbrandon@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'questions', QuestionView, 'question')
router.register(r'answers', AnswerView, 'answer')
router.register(r'categories', CategoryView, 'category')
router.register(r'playerresponses', PlayerResponseView, 'playerresponse')
router.register(r'reviews', ReviewView, 'review')
router.register(r'players', PlayerView, 'player')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui')
]

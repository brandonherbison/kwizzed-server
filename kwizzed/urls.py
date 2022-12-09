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
from rest_framework import routers
from kwizzedapi.views import register_user, login_user, QuestionView, AnswerView, CategoryView, PlayerResponseView, ReviewView, PlayerView

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
]

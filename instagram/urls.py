from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from instagram import views
from django.contrib.auth.models import User

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('public-posts', views.PostPublicViewSet)
router.register('private-posts', views.PostPrivateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('upload/', views.PostView.as_view()),
    path('registration/', include('rest_auth.registration.urls')),
]

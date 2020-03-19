from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.PostViewSet, basename='posts')

urlpatterns = [
                  path('users/', views.UserList.as_view()),
                  path('users/<int:pk>/', views.UserDetail.as_view()),
                  path('like/', views.PostLikeUnlike.as_view())

              ] + router.urls

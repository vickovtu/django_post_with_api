from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('blog/<int:id>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('', views.post_list, name='post_list'),
    path('post_create/', views.post_create, name="post_create"),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('like/', views.like_post, name='like_post'),
    path('post_edit/<int:id>/', views.post_edit, name='post_edit'),
    path('post_delete/<int:id>/', views.post_delete, name='post_delete'),


    # password reset url
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/confirm/<str:uid64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password-reset/complete', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_complete'),

    path('', include('django.contrib.auth.urls'))
]

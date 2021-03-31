from django.contrib.auth import views
from django.urls import path, re_path
from .views import LoginView, SignupView, UserView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('<str:pk>/', UserView.as_view(), name='user_room'),
]
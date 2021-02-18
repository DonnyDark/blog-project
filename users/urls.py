from django.contrib.auth import views
from django.urls import path
from .views import LoginView, SignupView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('me/', UserView.as_view(), name='user'),
    # path('password_change/', PasswordChangeView.as_view(), name='password_change'),
]
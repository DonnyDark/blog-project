from django.urls import path
from .views import SignUpView, LogInView, UserView, PasswordChangeView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('me/', UserView.as_view(), name='user'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
]
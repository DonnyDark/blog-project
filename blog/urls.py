from django.urls import path
from .views import BlogListView, BlogCreateView, BlogDetailView


urlpatterns = [
    path('', BlogListView.as_view(), name='main_page'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<uuid:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]
# web_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_page, name='product_page'),
    path('comment_history/', views.comment_history, name='comment_history'),
    # Add more paths as needed
]

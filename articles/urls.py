from django.urls import path
from . import views

urlpatterns = [
    path('recommend/<str:article_id>/', views.recommend_articles, name='recommend_articles'),
    path('article/<str:article_id>/', views.article_detail, name='article_detail'),
]
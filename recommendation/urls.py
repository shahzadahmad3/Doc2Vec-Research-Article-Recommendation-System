from django.urls import path
from . import views

urlpatterns = [
    path("by-article/<str:paper_id>/", views.recommend_by_article, name="recommend_by_article"),
    path("search/", views.recommend_by_query, name="recommend_by_query"),
]

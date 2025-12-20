from django.urls import path, include

from .views import ArticleCreateView, ArticleListView, PostDetailView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
     path('', ArticleListView.as_view(), name='articles_list'),
     path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
     path('create/', ArticleCreateView.as_view(), name='article_create'),
     path('<int:pk>/edit', ArticleUpdateView.as_view(), name='article_update'),
     path('<int:pk>/delete', ArticleDeleteView.as_view(),  name='article_delete'),

]
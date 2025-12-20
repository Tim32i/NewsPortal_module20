from django.urls import path, include

from .views import NewsListView, PostDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, \
                   NewsFilteredListView

urlpatterns = [
     path('', NewsListView.as_view(), name='news_list'),
     path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
     path('create/', NewsCreateView.as_view(), name='post_create'),
     path('<int:pk>/edit/', NewsUpdateView.as_view(), name='update_news'),
     path('<int:pk>/delete', NewsDeleteView.as_view(), name='delete_news'),
     path('search/', NewsFilteredListView.as_view(), name='filtered_news')
]
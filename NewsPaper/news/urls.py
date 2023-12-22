from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewsCreate, NewsDelete, NewsUpdate, ArticlesUpdate, ArticlesDelete, \
   IndexView, upgrade_me, ArticlesCreate, CategoryListView, subscribe

urlpatterns = [
   path('', PostList.as_view(), name='news'),
   path('index', IndexView.as_view(), name='profile'),
   path('search/', PostSearch.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='separate_news'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
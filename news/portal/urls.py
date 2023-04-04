from django.urls import path
# Импортируем созданное нами представление
from .views import (
    PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView,PostSearch,
)

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='product_list'),

   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/',  PostCreateView.as_view(), name='article_add'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
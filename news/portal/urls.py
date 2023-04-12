from django.urls import path
from django.conf import settings
from django.shortcuts import redirect
# Импортируем созданное нами представление
from .views import (
    PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView,PostSearch,BaseRegisterView
)
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me
from .views import IndexView
urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='product_list'),
   #path('protected/', ProtectedView.as_view(), name='protected_page'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/',  PostCreateView.as_view(), name='article_add'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
   path('login/',
        LoginView.as_view(template_name='news/login.html'),
        name='login'),
   path('logout/',
        LogoutView.as_view(template_name='news/logout.html'),
        name='logout'),
   path('signup/',
        BaseRegisterView.as_view(template_name='news/signup.html'),
        name='signup'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('', IndexView.as_view()),
]
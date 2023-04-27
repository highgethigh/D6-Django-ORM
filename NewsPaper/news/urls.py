from django.urls import path
# импортируем наше представление
from .views import PostList, PostDetail, PostCreateView, PostDeleteView, PostUpdateView, CategoryList, CategoryDetail, add_subscribe, del_subscribe
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    # # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    path('', cache_page(60*1) (PostList.as_view())), # кэшируем все новости на 1 минуту
    path('<int:pk>', cache_page(60 * 5)(PostDetail.as_view()), name='post'),  # pk — это первичный ключ новости, который будет выводиться у нас в шаблон, кэшируем отдельную новость на 5 минут
    path('search/', views.search, name='search'),
    path('add/', PostCreateView.as_view(), name='post_create'), # ссылка на создание новости/статьи
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('categories/', CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category_subscription'),
    # Функция-представление для подписки на выбранную категорию
    path('categories/<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    # Функция-представление для отписки от выбранной категории
    path('categories/<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]



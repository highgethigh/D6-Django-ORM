# D7-Django-ORM Cache
# Перед запуском проекта запустить виртуальное окружение через консоль:
```
    source venv/bin/activate
```
### Задание:
1. Добавьте кэширование на страницы с новостями (по 5 минут на каждую) и на главную страницу (одну минуту).
2. В шаблонах постарайтесь кэшировать все навигационные элементы (меню, сайдбары и так далее). Количество кэшируемого времени остаётся на ваше усмотрение. Кроме того, можете использовать любую систему кэширования, какая вам более по нраву.

## P.S. для корректной работы, нужно добавить в <i>setting.py</i> почту для отправки сообщений пользователю!

### И небольшие изменения понадобится добавить в настройки:
```
    CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}
Плюс добавить в проекте папку, где будут храниться наш кэш "cache_files"
```
### Если у вас есть в проекте представления (<b>views</b>), оформленные через функции, тогда кэширование будет выполняться очень просто:
```
    from django.views.decorators.cache import cache_page # импортируем декоратор для кэширования отдельного представления
 
    @cache_page(60 * 15) # в аргументы к декоратору передаём количество секунд, которые хотим, чтобы страница держалась в кэше. Внимание! Пока страница находится в кэше, изменения, происходящие на ней, учитываться не будут!
    def my_view(request):
        ...
```

### Если вы используете классовые представления или дженерики, то нужно добавлять кэширование напрямую в <b>urls.py</b> (в котором хранятся именно сами представления, а не основной urls.py из папки с <b>settings.py</b>).
    Делается это следующим образом:
```
    from django.urls import path
    from .views import Products, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
    from django.views.decorators.cache import cache_page
     
     
    urlpatterns = [
        path('', Products.as_view()),
        path('<int:pk>/', cache_page(60*10)(ProductDetailView.as_view()), name='product_detail'), # добавим кэширование на детали товара. Раз в 10 минут товар будет записываться в кэш для экономии ресурсов.
        path('create/', ProductCreateView.as_view(), name='product_create'), 
        path('<int:pk>/update', ProductUpdateView.as_view(), name='product_update'), 
        path('<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'), 
    ]
```

### Для того, чтобы загрузить кэширование в HTML-шаблон, во-первых, кэширование уже должно быть настроено у вас в приложении, а во-вторых, должен быть загружен сам кэш с помощью тега <b>{% load cache %}</b>.
```
    {% load cache %} <!-- Загружаем кэширование -->
    {% cache 30 header %} <!-- Кэшируем отдельный блок на 30 секунд -->
        {% block header %}
        {% endblock header %}
    {% endcache %}
```
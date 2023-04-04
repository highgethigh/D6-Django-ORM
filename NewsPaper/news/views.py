# импортируем класс "дженерик"
# который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# импортируем модель пост
from .models import Post, PostCategory, Category
from datetime import datetime
# импортируем класс "paginator"
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# создадим модель объектов, которые будем выводить
class PostList(ListView):
    # название модели из файла models.py
    model = Post # модель Post
    # ссылка на шаблон странички, в данном случае файл templates/news.html
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')  # новости выводятся от старой до самой новой
    paginate_by = 10 # устанавливаем пагинацию на последние добавленные 10 новостей/статей

    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


# создаём представление, в котором будут детали конкретной отдельной новости/статьи
class PostDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получить детали конкретно отдельного поста
    template_name = 'post.html'  # название шаблона будет post.html
    context_object_name = 'post'  # название объекта


from django.shortcuts import render, redirect
from .search import PostFilter
def search(request):
    listings = Post.objects.all()
    listing_filter = PostFilter(request.GET, queryset=listings)
    context = {
        'listing_filter': listing_filter,
    }
    return render(request, "search.html", context)


from django.contrib.auth.mixins import PermissionRequiredMixin
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')



from django.contrib.auth.mixins import LoginRequiredMixin
# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'post_edit.html'
    form_class = PostForm
    permission_required = ('news.add_post')

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    


    

# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.add_post')



# класс-представление для списка категорий
# унаследован от стандартного представления
class CategoryList(ListView):
    model = Category  # указываем модель из которой берем объекты
    template_name = 'category_list.html'  # указываем имя шаблона, в котором написан html для отображения объектов модели
    context_object_name = 'categories'  # имя переменной, под которым будет передаваться объект в шаблон



# класс-представление для отображения списка категорий
# унаследован от стандартного представления
class CategoryDetail(DetailView):
    # указываем модель (таблицу базы данных)
    model = Category
    # указываем имя шаблона
    template_name = 'category_subscription.html'

    # для отображения кнопок подписки (если не подписан: кнопка подписки - видима, и наоборот)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # общаемся к содержимому контекста нашего представления
        category_id = self.kwargs.get('pk') # получаем ИД поста (выдергиваем из нашего объекта из модели Категория)
        # формируем запрос, на выходе получим список имен пользователей subscribers__username, которые находятся
        # в подписчиках данной группы, либо не находятся
        category_subscribers = Category.objects.filter(pk=category_id).values('subscribers__username')
        # Добавляем новую контекстную переменную на нашу страницу, выдает либо правду, либо ложь, в зависимости от
        # нахождения нашего пользователя в группе подписчиков subscribers
        context['is_not_subscribe'] = not category_subscribers.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = category_subscribers.filter(subscribers__username=self.request.user).exists()
        return context


# функция-представление обернутая в декоратор
# для добавления пользователя в список подписчиков
@login_required
def add_subscribe(request, **kwargs):
    # получаем первичный ключ выбранной категории
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    # добавляем в выбранную категорию, в поле "подписчики" пользователя, который авторизован и делает запрос
    Category.objects.get(pk=pk).subscribers.add(request.user)
    # возвращаемся на страницу со списком категорий
    return redirect('/news/categories/')


# функция-представление обернутая в декоратор
# для удаления пользователя из списка подписчиков
@login_required
def del_subscribe(request, **kwargs):
    # получаем первичный ключ выбранной категории
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    # удаляем в выбранной категории, из поля "подписчики" пользователя, который авторизован и делает запрос
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    # возвращаемся на страницу со списком категорий
    return redirect('/news/categories/')

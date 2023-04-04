from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'



from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def become_to_authors(request):
    # мы получили объект текущего пользователя из переменной запроса
    user = request.user
    # Вытащили author-группу из модели Group
    authors_group = Group.objects.get(name='authors')
    # проверяем, находится ли пользователь в этой группе
    if not request.user.groups.filter(name='authors').exists():
        # если он все-таки еще не в ней — смело добавляем.
        authors_group.user_set.add(user)
    return redirect('/')
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


# пользователь может подписаться и стать автором и попасть в группу authors и редактировать/добавлять/удалять новости/статьи
@login_required
def become_to_authors(request):
    user = request.user
    authors_group = Group.objects.get(name = 'authors')
    if not request.user.groups.filter(name = 'authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

# пользователь может подписаться на рассылку и войти в группу subcribers
@login_required
def become_to_subscribers(request):
    user = request.user
    subscribers_group = Group.objects.get(name = 'subscribers')
    if not request.user.groups.filter(name = 'subscribers').exists():
        subscribers_group.user_set.add(user)
    return redirect('/')
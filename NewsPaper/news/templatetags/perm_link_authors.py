from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# для сокрытия ссылки Add your news у пользователя, который не состоит в группе автор
# при написании может возникнуть ошибку, но нужно перезагрузить сервер
# в шаблоне {% load perm_link_authors %}
# {% if request.user|has_group("authors") %} Add your news {% endif%}
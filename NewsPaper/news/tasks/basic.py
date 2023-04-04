# Module D6.4
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def get_subscriber(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email


def new_post_subscription(instance):
    template = 'news/news_post.html'

    for post_link_category in instance.post_link_category.all():
        email_subject = f'New post in category: "{post_link_category}"'  # тема письма
        user_email = get_subscriber(post_link_category)

        html = render_to_string(
            template_name=template,
            context={
                'post_link_category': post_link_category,
                'post': instance,
            },
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_email
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
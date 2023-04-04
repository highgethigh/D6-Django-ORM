# Module D6.5

import logging

from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from datetime import timedelta

from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution



# отправка писем для подписчиков по категориям
from NewsPaper import settings
from ...models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def send_weekly_newsletter():
    # Формируем список новостей за неделю
    start = timezone.now().date() - timedelta(weeks=1)
    finish = timezone.now().date()
    posts = Post.objects.filter(post_data__range=(start, finish))


    # Получаем список категорий и подписчиков на каждую категорию
    categories = Category.objects.all()
    for category in categories:
        subscribers = User.objects.filter(subscriber__name_category=category)
        subscriber_emails = [subscriber.email for subscriber in subscribers]

        # Формируем текст сообщения
        message = render_to_string('news/week_news.html', {'posts': posts, 'category': category})



        # Отправляем сообщение на почту подписчиков
        email = EmailMultiAlternatives(
            'Weekly Newsletter',
            message,
            settings.DEFAULT_FROM_EMAIL,
            subscriber_emails
        )
        email.content_subtype = 'html'
        email.send()

    logger.info('Еженедельная рассылка успешно отправлена')


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем задачу на отправку еженедельной рассылки
        scheduler.add_job(
            send_weekly_newsletter,
            trigger=IntervalTrigger(weeks=1), # отправка каждую неделю
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'send_weekly_newsletter'.")

        # Добавляем задачу на удаление старых задач из базы данных
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'delete_old_job_executions'.")

        scheduler.start()


from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
import datetime
from .models import PostCategory, Post, Category


@shared_task
def send_notifications(preview, pk, heading, subscriber):
    html_content = render_to_string(
        'email_post_created.html',
        {
            'text':preview,
            'link': f'{settings.SITE_URL}/news/post/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject = heading,
        body='',
        from_email= settings.DEFAULT_FROM_EMAIL,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscriber: list[str]=[]
        for category in categories:
            subscriber += category.subscriber.all()

        subscriber = [s.email for s in subscriber]

        send_notifications(instance.preview(), instance.pk, instance.heading, subscriber)


@shared_task
def notify_weekly():
    today = datetime.datetime.now()
    last_week=today-datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list("subscribers__email", flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject="Posts on week",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory



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


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscriber: list[str]=[]
        for category in categories:
            subscriber += category.subscriber.all()

        subscriber = [s.email for s in subscriber]

        send_notifications(instance.preview(), instance.pk, instance.heading, subscriber)
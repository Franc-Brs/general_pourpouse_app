"""
Celery tasks
"""
from __future__ import absolute_import
from celery import shared_task
from core.models import Chiamate
from django.db.models import Q
import requests

from django.core.mail import send_mail
from django.conf import settings


def only_one(function=None, key="", timeout=None):
    """Enforce only one celery task at a time."""

    def _dec(run_func):
        """Decorator."""

        def _caller(*args, **kwargs):
            """Caller."""
            ret_value = None
            have_lock = False
            lock = settings.REDIS_CLIENT.lock(key, timeout=timeout)
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    ret_value = run_func(*args, **kwargs)
            finally:
                if have_lock:
                    lock.release()

            return ret_value

        return _caller

    return _dec(function) if function is not None else _dec


headers_1 = {
  'Accept': 'application/xml'
}


@shared_task(
    name='invio_chiamate',
    bind=True,
    autoretry_for=(Exception,),
    # togliere backoff e viene una chiamata ogni 3 min, quindi 18 min in tutto
    # tra una chiamata e l'altra
    retry_kwargs={'max_retries': 5, 'default_retry_delay': 3},
    # in test
    retry_backoff=True,
)
@only_one(key="SingleTask", timeout=60 * 5)
def invio_chiamate(self):
    try:

        chiamate = (
            Chiamate.objects.all()
            .filter(
                Q(status=settings.STATUS['negative_response']) |
                Q(status=settings.STATUS['sent'])
            )
            .order_by("status", "id")
            .first()
        )

        if chiamate is None:
            print("no requests to process or enqueue")
            return

        print(f"Id: {chiamate.id}, chiamata: {chiamate.chiamata }")

        response = requests.request(
            'POST',
            chiamate.server,
            # headers=settings.HEADERS,
            headers=headers_1,
            data=chiamate.chiamata
        )
        response.raise_for_status()

        # useless if
        if response.status_code == 200:
            print("status 200")
            Chiamate.objects.filter(id=chiamate.id).update(
                status=settings.STATUS['positive_response'],
                risposta_server_terzo=response.text
            )
            return f"{chiamate.id} has positive response"

    except Exception as err:

        print(err)
        Chiamate.objects.filter(id=chiamate.id).update(
                status=settings.STATUS['negative_response'],
                risposta_server_terzo=response.text
        )

        if self.request.retries == 5:

            mail_body = f"""\
                      Automatic Email:

                      Check task nr {chiamate.id},
                      Sending request to third-party services is failed
                      """

            send_mail(
                subject='Coda invio info a third-party services bloccata',
                message=mail_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS]
            )
            print("sent mail")
        raise Exception()

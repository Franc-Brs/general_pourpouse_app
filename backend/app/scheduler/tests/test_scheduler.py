"""
Test for scheduler
"""
# from django.contrib.auth import get_user_model
# from django.test import TestCase
from django.test import TransactionTestCase

# from core.models import Chiamate
from scheduler.tasks import invio_chiamate
from core.models import Chiamate
from datetime import datetime
import pytz

from django.conf import settings


def create_chiamata(**params):
    """Helper function: create and return a sample chiamata (one row)"""

    h_now = datetime.now(
                pytz.timezone('Europe/Rome')
    ).isoformat(timespec='seconds')

    defaults = {
        'datetime_creation': f"{h_now}",
        'datetime': f"{h_now}",
        'chiamata': '''
                    <?xml version='1.0' encoding='utf-8'?><Request>
                        <Login>login</Login>
                    </Request>
                    ''',
        'status': settings.STATUS['sent'],
        'server': 'https://httpbin.org/anything',
        'risposta_server_terzo': '',
    }
    defaults.update(params)

    chiamata = Chiamate.objects.create(**defaults)
    return chiamata


class SchedulerTest(TransactionTestCase):
    """ Test celery task."""

    reset_sequences = True

    def test_task_without_db(self):
        """ Test celery task without row in db."""
        task = invio_chiamate.s().apply()

        # why
        self.assertEqual(task.status, 'SUCCESS')

    def test_task_with_ok_row(self):
        """ Test task with one row that is processed correctly."""
        create_chiamata()
        task = invio_chiamate.s().apply()
        print(task.result)

        # why
        self.assertEqual(task.status, 'SUCCESS')

    def test_task_with_not_ok_row(self):
        """ Test task with one row that is not processed correctly."""
        payload = {
                'status': settings.STATUS['negative_response'],
                'server': 'https://httpbin.org/anythingeee',
        }
        create_chiamata()
        create_chiamata(**payload)
        create_chiamata()

        task = invio_chiamate.s().apply()
        rejected = Chiamate.objects.all().filter(
            status=settings.STATUS['negative_response']
        )

        self.assertEqual(task.status, 'FAILURE')
        self.assertEqual(rejected.count(), 1)
        self.assertEqual(rejected.first().id, 2)

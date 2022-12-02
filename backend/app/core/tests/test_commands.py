"""
Test custom Django management commands.
"""
# we'll mock the behaviour of the Db as we need to simulate DB response or not
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# BaseCommand has a check method that allow us to check the status of db
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        # this ensures that the mocked value (of the decorator) is called
        # with the defualt db
        patched_check.assert_called_once_with(databases=['default'])

    # with this patch we override and mock behaviour of sleep so it
    # does not pause the code
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""

        # The firsts two times we call the mocked method it should raise
        #  psycopg2 error
        # then we raise 3 OperationalError (coz there are diff stages of
        # Postgresql starting)
        # so sometimes, db is up but it does not have put up the test db
        # that we want to use
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

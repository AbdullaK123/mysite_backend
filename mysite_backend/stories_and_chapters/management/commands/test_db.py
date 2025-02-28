# api/management/commands/test_db.py
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Tests the database connection'

    def handle(self, *args, **options):
        try:
            db_conn = connections['default']
            db_conn.cursor()
            self.stdout.write(self.style.SUCCESS('Database connection working!'))
        except OperationalError:
            self.stdout.write(self.style.ERROR('Database connection failed!'))
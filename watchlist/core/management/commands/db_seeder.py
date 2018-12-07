from django.core.management.base import BaseCommand
from core.models import Role, WatchlistPermission


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.seed_roles()
        self.seed_watchlist_permissions()
        self.stdout.write(self.style.SUCCESS(
            'Database seeded successfully'))

    @staticmethod
    def seed_roles():
        admin = Role()
        admin.name = 'admin'
        admin.save()

        audience = Role()
        audience.name = 'watcher'
        audience.save()

    @staticmethod
    def seed_watchlist_permissions():
        permission = WatchlistPermission()
        permission.name = 'Owner'
        permission.save()

        permission = WatchlistPermission()
        permission.name = 'Edition'
        permission.save()

        permission = WatchlistPermission()
        permission.name = 'View'
        permission.save()


from django.core.management.base import BaseCommand
from authentication.models import InterfaceUser


class Command(BaseCommand):
    help = 'Create a new Admin'

    def handle(self, *args, **options):
        name = input('Enter name for the Admin user: ')
        email = input('Enter email for the Admin user: ')
        password = input('Enter password for the Admin user: ')

        try:
            superadmin_user = InterfaceUser.objects.create_admin(email, name, password)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Admin user {superadmin_user.name} ({superadmin_user.email}) created successfully'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating Admin user: {e}'))
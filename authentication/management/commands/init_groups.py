from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from typing import List, Type, Set
from tracks.models import Track, Artist, Metadata, MetadataValue, MetadataOption
from multimedia.models import TrackImage, ArtistImage, AudioFile
from authentication.models import InterfaceUser


class Command(BaseCommand):
    help = 'Initialize and update user groups with appropriate permissions'

    # Define permission configuration as a class attribute
    PERMISSION_CONFIG = {
        'Admin': {
            'models': {
                Track: ['add', 'change', 'delete', 'view'],
                Artist: ['add', 'change', 'delete', 'view'],
                Metadata: ['add', 'change', 'delete', 'view'],
                MetadataValue: ['add', 'change', 'delete', 'view'],
                MetadataOption: ['add', 'change', 'delete', 'view'],
                TrackImage: ['add', 'change', 'delete', 'view'],
                ArtistImage: ['add', 'change', 'delete', 'view'],
                AudioFile: ['add', 'change', 'delete', 'view'],
                InterfaceUser: ['add', 'change', 'delete', 'view'],
            }
        },
        'User': {
            'models': {
                Track: ['view'],
                Artist: ['view'],
                MetadataOption: ['view'],
                AudioFile: ['view'],
                InterfaceUser: ['view', 'change'],  # Users can view and edit their own profiles
            }
        }
    }

    def get_model_permissions(self, model: Type[Model], actions: List[str]) -> Set[Permission]:
        """Get all permissions for a model based on specified actions."""
        content_type = ContentType.objects.get_for_model(model)
        permissions = set()
        for action in actions:
            perm_codename = f'{action}_{model._meta.model_name}'
            try:
                permission = Permission.objects.get(
                    content_type=content_type,
                    codename=perm_codename
                )
                permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Permission {perm_codename} does not exist for {model.__name__}'
                    )
                )
        return permissions

    def update_group_permissions(self, group: Group, required_permissions: Set[Permission]):
        """Update group permissions incrementally."""
        current_permissions = set(group.permissions.all())
        
        # Permissions to add
        permissions_to_add = required_permissions - current_permissions
        if permissions_to_add:
            group.permissions.add(*permissions_to_add)
            for perm in permissions_to_add:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Added permission "{perm.codename}" to group "{group.name}"'
                    )
                )

        # Permissions to remove
        permissions_to_remove = current_permissions - required_permissions
        if permissions_to_remove:
            group.permissions.remove(*permissions_to_remove)
            for perm in permissions_to_remove:
                self.stdout.write(
                    self.style.WARNING(
                        f'Removed permission "{perm.codename}" from group "{group.name}"'
                    )
                )

    def handle(self, *args, **options):
        for group_name, config in self.PERMISSION_CONFIG.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group "{group_name}"')
                )

            # Collect all required permissions for this group
            required_permissions = set()
            for model, actions in config['models'].items():
                model_permissions = self.get_model_permissions(model, actions)
                required_permissions.update(model_permissions)

            # Update the group's permissions
            self.update_group_permissions(group, required_permissions)

        self.stdout.write(self.style.SUCCESS('Finished updating groups and permissions'))

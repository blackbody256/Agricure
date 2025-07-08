from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # Hardcoded admin credentials
        admin_username = 'admin'
        admin_email = 'admin@agricure.com'
        admin_password = 'adminpassword123'
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name='Admin',
                last_name='User',
                role='ADMIN'
            )

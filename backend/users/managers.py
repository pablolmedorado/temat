from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    def active(self):
        return self.filter(is_active=True)

    def admins(self):
        return self.filter(is_superuser=True)

    def get_random_admin(self):
        return self.admins().first()

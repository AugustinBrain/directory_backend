from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdminAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, permission='admin'):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            permission=permission
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
            permission='superadmin'
        )
        return user

class AdminAccount(AbstractBaseUser):
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'
    
    PERMISSION_CHOICES = [
        (ADMIN, 'Admin'),
        (SUPERADMIN, 'Super Admin'),
    ]
    
    account_id = models.CharField(primary_key=True, max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    img_path = models.CharField(max_length=255, null=True, blank=True)
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES, default=ADMIN)
    
    objects = AdminAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def is_superadmin(self):
        return self.permission == self.SUPERADMIN
    
    @property
    def is_admin(self):
        return self.permission == self.ADMIN
    
    # Required for Django admin
    @property
    def is_staff(self):
        return self.is_superadmin
    
    @property
    def is_superuser(self):
        return self.is_superadmin
    
    def has_perm(self, perm, obj=None):
        return self.is_superadmin
    
    def has_module_perms(self, app_label):
        return self.is_superadmin
    
    class Meta:
        db_table = '"admin"."admin_account"'
        verbose_name = "Admin Account"
        verbose_name_plural = "Admin Accounts"
        managed = False


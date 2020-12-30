from django.db import models

# add
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

# add
class UserManager(BaseUserManager):
    use_in_migrations = True

    # def _create_user(self, username, email, password, **extra_fields):
    def _create_user(self, email, password, **extra_fields):
        # """
        # Create and save a user with the given username, email, and password.
        # """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        # username = self.model.normalize_username(username)
        # user = self.model(username=username, email=email, **extra_fields)
        user = self.model( email=email,   **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_user(self, username, email=None, password=None, **extra_fields):
    def create_user(self,  email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self,  email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # return self._create_user(username, email, password, **extra_fields)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # """
    # An abstract base class implementing a fully featured User model with
    # admin-compliant permissions.
    # Username and password are required. Other fields are optional.
    # """
    ##***username_validator = UnicodeUsernameValidator()

    # username = models.CharField(
    #     _('username'),
    #     max_length=150,
    #     unique=True,
    #     help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #     validators=[username_validator],
    #     error_messages={
    #         'unique': _("A user with that username already exists."),
    #     },
    # )
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True,unique=True)
    # profile = models.CharField(_('profile'), max_length=255, blank=True) # add
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


    objects = UserManager()

    EMAIL_FIELD = 'email' # fix
    USERNAME_FIELD = 'email' # fix
    # REQUIRED_FIELDS = ['username'] # fix
    # REQUIRED_FIELDS = ['email']  # fix

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        # """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

# アップロードされたファイルを一意の名前にする
def upload_path(instance, filename):
    # 拡張子の取得
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.userPro.id)+str(instance.nickName)+str(".")+str(ext)])


class Profile(models.Model):
    nickName = models.CharField(max_length=20 ,blank=True, null=True)
    userPro = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userPro',
        on_delete=models.CASCADE
    )
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_path)

    def __str__(self):
        return self.nickName

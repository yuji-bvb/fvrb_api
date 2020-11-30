from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.userPro.id)+str(instance.nickName)+str(".")+str(ext)])


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class FrameBrand(models.Model):
    item = models.CharField(max_length=30)

    def __str__(self):
        return self.item


class WheelBrand(models.Model):
    item = models.CharField(max_length=30)

    def __str__(self):
        return self.item


class Profile(models.Model):
    COMPONENT = (
        ("1", "SHIMANO"),
        ("2", "SRAM"),
        ("3", "CAMPAGNOLO"),
    )
    nickName = models.CharField(max_length=20)
    frameBrand = models.ForeignKey(FrameBrand, on_delete=models.CASCADE)
    frame = models.CharField(max_length=30, null=True, default="IMPULSO")
    component = models.CharField(max_length=40, choices=COMPONENT, default="1")
    compo = models.CharField(max_length=30, null=True, default="105")
    wheelBrand = models.ForeignKey(WheelBrand, on_delete=models.CASCADE)
    wheel = models.CharField(max_length=30, null=True, default="Z LITE PBO pink")
    purchase = models.DateField(null=True)
    userPro = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userPro',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked", blank=True)
    favCourse = models.CharField(max_length=100, null=True, default="成木")
    favGear = models.CharField(max_length=100, null=True, default="")
    favShop = models.CharField(max_length=50, null=True, default="8823福生店")

    def __str__(self):
        return self.nickName


class FriendRequest(models.Model):
    askFrom = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='askFrom',
        on_delete=models.CASCADE
    )
    askTo = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='askTo',
        on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = (('askFrom', 'askTo'),)

    def __str__(self):
        return str(self.askFrom) + '----->' + str(self.askTo)


class Message(models.Model):

    message = models.CharField(max_length=140)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='receiver',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.sender)

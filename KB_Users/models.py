from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from tickets.models import Department


# Create your models here.


class UserKBManager(BaseUserManager):
    def create_user(self, userName, tabelNumber, password=None):
        """
        Creates and saves a User with the given username, date of
        birth and password.
        """
        if not (userName or tabelNumber):
            raise ValueError('Users must have an username and tabel number')

        user = self.model( userName=userName, tabelNumber=tabelNumber)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userName, tabelNumber, password):
        """
        Creates and saves a superuser with the given username, date of
        birth and password.
        """
        user = self.create_user(userName, tabelNumber, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserKB(AbstractBaseUser):
    userName = models.CharField(max_length=20,
                                unique=True,
                                help_text = 'Ваш псевдоним используется только для входа на сайт' )
    firstName = models.CharField('Имя', max_length=20)
    secondName = models.CharField('Фамилия', max_length=30)
    fathName =  models.CharField('Отчество', max_length=30)
    tabelNumber = models.IntegerField('Табельный №',
                                      help_text='Табельный номер используется для дополнительной идентификации пользователя или при восстановлении доступа',
                                      unique = True)
    phone = models.CharField('Телефон', max_length=10)
    department = models.ForeignKey('tickets.Department',verbose_name='Подразделение', on_delete='SET_NULL', max_length=10, null=True)

    email = models.EmailField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, editable=False)

    objects = UserKBManager()

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = ['tabelNumber']

    #news = models.

    def get_full_name(self):
        # The user is identified by their full name
        return str(self.firstName) + ' ' + str(self.secondName)

    def get_short_name(self):
        # The user is identified by their username
        return self.userName

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        if self.firstName and self.secondName and self.fathName:
            return self.secondName + ' ' + str(self.firstName)[0] + '.' + str(self.fathName)[0] + '.'
        return self.userName

    def is_boss(self):
        return self.id in Department.objects.all().values_list('boss', flat=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['secondName']
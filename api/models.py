from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.timezone import now
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models import \
    CharField, UUIDField, Model, IntegerField, DateTimeField, \
    BooleanField, ManyToManyField, TextField, EmailField, \
    ForeignKey, FloatField, OneToOneRel, PROTECT, OneToOneField, ManyToOneRel

from django.utils.translation import ugettext_lazy as _
import uuid
from django.db.models import Sum
from django.db.models import Q
from .validators import tin_validator, pay_validator
from django.db import transaction
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class BaseModel(Model):
    class Meta:
        abstract = True

    id = UUIDField(db_column='Id', primary_key=True, default=uuid.uuid4)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class EUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not date_of_birth:
            date_of_birth = now()

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not email:
            email = 'ivanvalenkov@gmail.com'
        if not date_of_birth:
            date_of_birth = now()

        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CashTransaciton(BaseModel):
    class Meta:
        verbose_name = _("currency transfers")
        verbose_name_plural = _("currency transfers")

    tid = UUIDField(primary_key=False, default=uuid.uuid4,
                    unique=False,  # may be many recipients
                    null=False, db_index=True)

    val = FloatField(help_text="currency", validators=[pay_validator],
                     verbose_name="Amount transfer", )
    src = ForeignKey("EUser", related_name="src_user_id", on_delete=PROTECT, null=True, default=None, blank=True)
    dst = ForeignKey("EUser", related_name="dst_user_id", on_delete=PROTECT, null=True, default=None)
    active = BooleanField(verbose_name="Active", db_index=True, help_text="Transaction accepted", default=True)

    # test = IntegerField(verbose_name='test')

    def __str__(self):
        return f"tid: {self.tid} src:{self.src} to {self.dst} amount:{self.val} Active:{self.active}"

    def activate(self) -> bool:
        raise NotImplementedError("TODO")

    def deactivate(self) -> bool:
        # Распроведение одиночной транзакции
        raise NotImplementedError("TODO")

    def deactivate_cascade(self):
        # Каскадное распроведение переводов
        raise NotImplementedError("TODO")


class EUser(AbstractUser, BaseModel):
    middle_name = CharField(_('Отчество'), max_length=30, blank=True, null=True
                            )

    tin = CharField(_("ИНН"), unique=False, blank=False, null=False, validators=[tin_validator], max_length=12,
                    help_text="10 or 12 digits", db_index=True)

    # кешированное поле
    cached_balance = FloatField(_('cached balance'), db_index=True, null=True, blank=True, unique=False,
                                help_text="This field is cache of CashTransactions. Please rebuild.")

    @property
    def transactions(self):
        return CashTransaciton.objects.filter(Q(src=self) | Q(dst=self)).all()

    # REQUIRED_FIELDS = []
    class Meta:
        # db_table = "User"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def balance(self):
        c = cache.get(self.id)
        if c:
            return c
        else:
            balance = self.balance_rebuild()
            self.cached_balance = balance
            self.save()
            return balance

    def get_credit_transactions(self):
        return CashTransaciton.objects.filter(dst=self, active=True)

    def get_credit(self) -> float:
        ret = self.get_credit_transactions().aggregate(Sum('val'))['val__sum'] or 0
        return ret

    def get_debt_transactions(self):
        return CashTransaciton.objects.filter(src=self, active=True)

    def get_debt(self) -> float:
        return self.get_debt_transactions().aggregate(Sum('val'))['val__sum'] or 0

    def balance_rebuild(self) -> float:
        ret = self.get_credit() - self.get_debt()
        self.cached_balance = ret
        self.save()
        return ret

    @staticmethod
    def balance_rebuild_for_all():
        # TODO: Временное решение для тестирования. Это нужно оптимизировать, например sql процедурой.
        for u in EUser.objects.all():
            u.balance_rebuild()

    def make_receipt(self, val: float):
        """
        сделать поступление
        :param val:
        :return:
        """

        logger.info(f'start EUser:make_reciept +{val}')
        t = CashTransaciton(val=float(val), src=None, dst=self)
        t.save()

    def make_expense(self, val: float) -> bool:
        """
        сделать списание
        :param val:
        :return:
        """
        # expended val checks in validator
        t = CashTransaciton(val=val, src=self, dst=None)
        try:
            t.save()
            return True
        except ValueError:
            return False

    @transaction.atomic
    def make_transfer(self, val, user=None, tin: str = None) -> bool:
        """
        Перевод для пользователя, или для нескольких по инн
        :param val:
        :param user:
        :param tin:
        :return:
        """
        if user is not None and tin is not None:
            raise AssertionError("Недопустимая ситуация, когда при переводе указан пользователь и инн")
        else:
            if user:
                try:
                    CashTransaciton(val=val, src=self, dst=user).save()
                    return True
                except AssertionError:
                    return False
                except:
                    return False
            else:
                users = EUser.objects.filter(tin=tin)
                cnt = len(users)
                part = round(val / cnt, 2)
                sid = transaction.savepoint()
                for u in users:
                    if not self.make_transfer(part, user=u):
                        transaction.savepoint_rollback(sid)
                        return False
                transaction.savepoint_commit(sid)
                return True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        return full_name.strip()

    @staticmethod
    def _split_name(s='', i=0):
        # Фадеева         Лариса         Константиновна
        s = s.replace('  ', ' ')
        spl = s.split(' ')
        try:
            ret = spl[i]
        except Exception:
            ret = None
        return ret

    @classmethod
    def extract_first_name(cls, s=''):
        return cls._split_name(s, 1)

    @classmethod
    def extract_last_name(cls, s=''):
        return cls._split_name(s, 0)

    @classmethod
    def extract_middle_name(cls, s=''):
        return cls._split_name(s, 2)

    def __str__(self):
        return f"{self.username} : {self.balance} руб."

    def __repr__(self):
        return f" {self.id}: {self.get_full_name()}"


@receiver(pre_save, sender=CashTransaciton)
def _on_cash_transaction_pre_save(sender, instance: CashTransaciton, **kwargs):
    if instance.src and instance.src.balance < instance.val:
        raise AssertionError(_(f"Not enough user ({instance.src.get_full_name()}) money"))

    if not instance.src and not instance.dst:
        raise AssertionError(_(f"no src and no dst. Empty."))

    instance.updated_at = now()


@receiver(pre_save, sender=EUser)
def _on_user_pre_save(sender, instance: EUser, **kwargs):
    instance.updated_at = now()


@receiver(post_save, sender=CashTransaciton)
def _on_cash_transaction_post_save(sender, instance: CashTransaciton, **kwargs):
    if instance.active:
        if instance.src:
            cache.delete(instance.src.id)
        if instance.dst:
            cache.delete(instance.dst.id)


if settings.DEBUG:
    cache.clear()

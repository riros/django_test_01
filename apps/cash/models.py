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

from base.basemodel import BaseModel

from apps.cash.validators import pay_validator
from project import settings


class CashTransaciton(BaseModel):
    class Meta:
        verbose_name = _("currency transfers")
        verbose_name_plural = _("currency transfers")

    tid = UUIDField(primary_key=False, default=uuid.uuid4,
                    unique=False,  # may be many recipients
                    null=False, db_index=True)

    val = FloatField(help_text="currency", validators=[pay_validator],
                     verbose_name="Amount transfer", )
    src = ForeignKey("base.EUser", related_name="src_user_id", on_delete=PROTECT, null=True, default=None, blank=True)
    dst = ForeignKey("base.EUser", related_name="dst_user_id", on_delete=PROTECT, null=True, default=None)
    active = BooleanField(verbose_name="Active", db_index=True, help_text="Transaction accepted", default=True)

    # test = IntegerField(verbose_name='test') № иногда джанго не делает миграцию для подключенного приложения

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


@receiver(pre_save, sender=CashTransaciton)
def _on_cash_transaction_pre_save(sender, instance: CashTransaciton, **kwargs):
    if instance.src and instance.src.balance < instance.val:
        raise AssertionError(_(f"Not enough user ({instance.src.get_full_name()}) money"))

    if not instance.src and not instance.dst:
        raise AssertionError(_(f"no src and no dst. Empty."))

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

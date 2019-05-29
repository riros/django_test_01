from typing import AnyStr
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def tin_validator(inn: AnyStr):
    if len(inn) not in (10, 12):
        raise ValidationError(_(f"tin not 10 and no 12 digits {inn}"))

    def inn_csum(inn):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11 - len(inn):], [int(x) for x in inn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(inn) == 10:
        if not (inn[-1] == inn_csum(inn[:-1])):
            raise ValidationError(_(f"wrong csum tin fun2 {inn}"))

    else:
        if not (inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1])):
            raise ValidationError(_(f"wrong csum tin fun3 {inn}"))


def pay_validator(val):
    if val < 0:
        raise ValidationError(_(f"Credit  {val}<0 "))

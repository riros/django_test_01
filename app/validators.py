from typing import AnyStr


def inn_validator(inn: AnyStr) -> bool:
    if len(inn) not in (10, 12):
        return False

    def inn_csum(inn):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11 - len(inn):], [int(x) for x in inn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(inn) == 10:
        return inn[-1] == inn_csum(inn[:-1])
    else:
        return inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1])
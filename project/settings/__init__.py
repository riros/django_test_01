from .base import *

try:
    from .dev import *
    # print('dev env loaded')
except ImportError:
    from .prod import *
    print('Production! environment loaded.')

# print(STATIC_ROOT)

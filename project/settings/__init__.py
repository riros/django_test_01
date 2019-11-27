from .base import *

try:
    from .dev import *
except ImportError as e:
    from .prod import *

    print(e)
    print('Production environment loaded.')

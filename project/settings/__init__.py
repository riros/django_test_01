from .base import *

try:
    from .dev import *
except ImportError:
    from .prod import *

    print('Production environment loaded.')

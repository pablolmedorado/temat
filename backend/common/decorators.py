from functools import wraps

from django.db import transaction


def atomic_transaction_singleton(func):
    """
    Opens an atomic transaction block if the decorated function call is not
    already inside a transaction
    """

    def _use_atomic_savepoint():
        connection = transaction.get_connection()
        return not connection.in_atomic_block

    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction.atomic(savepoint=_use_atomic_savepoint()):
            return func(*args, **kwargs)

    return wrapper

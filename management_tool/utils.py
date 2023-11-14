import os
from django.core.exceptions import ImproperlyConfigured


TRUTHY_STRINGS = ("true", "yes", "on", "1")


def get_env_var(var_name, default=None):
    var = os.getenv(var_name, default)
    if var is None and default is None:
        raise ImproperlyConfigured(f"Set the {var_name} environment variable")

    return var


def get_bool_env_var(var_name, default=None):
    var = get_env_var(var_name, default)
    return var.lower() in TRUTHY_STRINGS


def get_int_env_var(var_name, default=None):
    var = get_env_var(var_name, default)
    try:
        return int(var)

    except ValueError:
        raise ImproperlyConfigured(
            f"Environment variable {var_name} "
            f"must be an integer or integer-convertible string"
        )

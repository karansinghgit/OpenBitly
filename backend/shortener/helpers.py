import re
import secrets


BASE_62_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Aliases share the redirect path, so they must be URL-safe and short enough to
# fit the Link.code column (max 10). Reserved names would shadow real routes.
ALIAS_RE = re.compile(r'^[A-Za-z0-9_-]{1,10}$')
RESERVED_CODES = {'api', 'admin', 'static'}


def is_valid_alias(alias):
    return bool(ALIAS_RE.fullmatch(alias)) and alias.lower() not in RESERVED_CODES

def generate_code(length=7):
    return "".join(secrets.choice(BASE_62_SET) for _ in range(length))

def unique_code(length=7):
    # random codes can collide, so keep trying until we find a free one.
    from .models import Link

    while True:
        code = generate_code(length)
        if not Link.objects.filter(code=code).exists():
            return code

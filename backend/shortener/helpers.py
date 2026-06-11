import secrets


BASE_62_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def generate_code(length=7):
    return "".join(secrets.choice(BASE_62_SET) for _ in range(length))

def unique_code(length=7):
    # random codes can collide, so keep trying until we find a free one.
    from .models import Link

    while True:
        code = generate_code(length)
        if not Link.objects.filter(code=code).exists():
            return code

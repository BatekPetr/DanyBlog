from itsdangerous import URLSafeTimedSerializer

from ...config import cfg


def generate_token(email):
    serializer = URLSafeTimedSerializer(cfg.SECRET_KEY)
    return serializer.dumps(email, salt=cfg.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(cfg.SECRET_KEY)
    try:
        email = serializer.loads(
            token, salt=cfg.SECURITY_PASSWORD_SALT, max_age=expiration
        )
        return email
    except Exception:
        return False

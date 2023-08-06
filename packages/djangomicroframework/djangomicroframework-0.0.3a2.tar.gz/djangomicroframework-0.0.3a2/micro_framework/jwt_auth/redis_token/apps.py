from django.apps import AppConfig


class RedisTokenConfig(AppConfig):
    name = 'micro_framework.jwt_auth.redis_token'
    verbose_name = "Redis JWT Token"

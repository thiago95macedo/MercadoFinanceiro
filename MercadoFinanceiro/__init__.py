from __future__ import absolute_import, unicode_literals

# Este irá garantir que o aplicativo Celery seja sempre importado quando
# Django for iniciado para que o `shared_task` use este aplicativo.
from .celery import app as celery_app

__all__ = ('celery_app',)
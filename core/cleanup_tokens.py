from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from core.models import EmailVerificationToken
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Deletes expired or used email verification tokens'

    def handle(self, *args, **kwargs):
        try:
            expired_or_used = EmailVerificationToken.objects.filter(
                models.Q(is_used=True) | models.Q(expires_at__lt=timezone.now())
            )
            count = expired_or_used.count()
            expired_or_used.delete()
            logger.info(f"Deleted {count} expired or used tokens")
            self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} tokens"))
        except Exception as e:
            logger.error(f"Error deleting tokens: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Error deleting tokens: {str(e)}"))
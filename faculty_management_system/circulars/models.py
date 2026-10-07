from django.conf import settings
from django.db import models

class Circular(models.Model):
    circular_number = models.CharField(max_length=50, unique=True)
    subject = models.CharField(max_length=250)
    content = models.TextField()
    attachment = models.FileField(upload_to="circulars/", blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.circular_number} - {self.subject}"

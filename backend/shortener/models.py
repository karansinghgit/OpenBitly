from django.db import models

class Link(models.Model):
    code = models.CharField(max_length=10, unique=True)
    long_url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} -> {self.long_url}"

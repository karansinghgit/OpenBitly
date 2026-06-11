from django.db import models

class Link(models.Model):
    code = models.CharField(max_length=10, unique=True)
    long_url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} -> {self.long_url}"


class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")
    created_at = models.DateTimeField(auto_now_add=True)
    referer = models.URLField(max_length=2000, blank=True)
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"{self.link.code} @ {self.created_at:%Y-%m-%d %H:%M:%S}"

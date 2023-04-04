from django.db import models

# Create your models here.


class PasswordRecord(models.Model):
    instance_id = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=255)
    generated_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.instance_id} - {self.username} - {self.created_at}"


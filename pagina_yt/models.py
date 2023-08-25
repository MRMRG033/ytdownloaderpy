from django.db import models

class UserIP(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    visit_count = models.PositiveIntegerField(default=1)  # Campo para el conteo de visitas

    def __str__(self):
        return self.ip_address

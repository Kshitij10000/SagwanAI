from django.db import models
from django.contrib.auth.models import User 
from Home.models import Broker

# Fyers Credentials Model
class FyersCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fyers_credentials')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    redirect_uri = models.URLField(max_length=1024) 
    response_type = models.CharField(max_length=50)
    state = models.CharField(max_length=255)
    access_token = models.CharField(max_length=1024, blank=True, null=True) 
    token_expiry = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)  # New Field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'broker')  # Ensures one set of credentials per broker per user

    def __str__(self):
        return f"{self.user.username} - {self.broker.name}"

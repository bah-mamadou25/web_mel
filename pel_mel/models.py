from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    
    def set_password(self, password):
        self.password = password
        
    def check_password(self, password):
        return self.password == password



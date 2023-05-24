from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def change_password(current_password, new_password, confirm_password):
        admin = User.objects.get(username='admin')  # Supposons que le nom d'utilisateur de l'admin est 'admin'

        if admin.check_password(current_password):
            if new_password == confirm_password:
                admin.set_password(new_password)
                admin.save()
                return "Mot de passe changé avec succès."
            else:
                return "Le nouveau mot de passe et la confirmation ne correspondent pas."
        else:
            return "Mot de passe actuel incorrect."

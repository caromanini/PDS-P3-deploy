from django.db import models

class Controlador(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Controlador {self.id}"

class Locker(models.Model):
    id = models.AutoField(primary_key=True)
    controller = models.ForeignKey(Controlador, on_delete=models.CASCADE)
    password = models.CharField(max_length=4)
    owner_email = models.EmailField()

    def __str__(self):
        return f"Locker {self.id} - Controlador {self.controller.id}"
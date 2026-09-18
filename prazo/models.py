from django.db import models


class Prazo(models.Model):
    id_prazo = models.AutoField(primary_key=True)
    dias_de_atraso = models.CharField(max_length=5)
    dias_suspensao = models.CharField(max_length=5)

    def __str__(self):
        return f'Prazo {self.id_prazo}'
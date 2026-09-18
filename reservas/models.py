from django.db import models
from usuarios.models import Usuario
from exemplares.models import Exemplar


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    data_reserva = models.DateField()
    status = models.CharField(max_length=15)

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='ID_usuario'
    )

    exemplar = models.ForeignKey(
        Exemplar,
        on_delete=models.CASCADE,
        db_column='ID_exemplar'
    )

    def __str__(self):
        return f'Reserva {self.id_reserva}'
    
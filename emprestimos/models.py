
from django.db import models
from django.utils import timezone

from exemplares.models import Exemplar
from usuarios.models import Usuario
from prazo.models import Prazo


class Emprestimo(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    previsao_devolucao = models.DateField()

    data_devolucao = models.DateField(
        null=True,
        blank=True
    )

    exemplar = models.ForeignKey(
        Exemplar,
        on_delete=models.CASCADE,
        db_column='ID_exemplar'
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='ID_usuario'
    )

    prazo = models.ForeignKey(
        Prazo,
        on_delete=models.CASCADE,
        db_column='ID_prazo'
    )

    @property
    def devolvido(self):
        return self.data_devolucao is not None

    @property
    def atrasado(self):
        if self.devolvido:
            return self.data_devolucao > self.previsao_devolucao

        return timezone.localdate() > self.previsao_devolucao

    @property
    def dias_restantes(self):
        if self.devolvido:
            return 0

        return (self.previsao_devolucao - timezone.localdate()).days

    def __str__(self):
        return f'Empréstimo {self.id}'

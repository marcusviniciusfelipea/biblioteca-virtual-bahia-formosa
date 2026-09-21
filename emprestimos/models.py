from django.db import models
from exemplares.models import Exemplar
from usuarios.models import Usuario
from prazo.models import Prazo


class Emprestimo(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    previsao_devolucao = models.DateField()

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

    def __str__(self):
        return f'Empréstimo {self.id}'
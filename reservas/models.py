
from django.db import models
from usuarios.models import Usuario
from livros.models import Livro


class Reserva(models.Model):

    STATUS_CHOICES = [
        ('Aguardando', 'Aguardando'),
        ('Disponível', 'Disponível'),
        ('Concluída', 'Concluída'),
        ('Cancelada', 'Cancelada'),
    ]

    id_reserva = models.AutoField(primary_key=True)

    data_reserva = models.DateField(auto_now_add=True)

    data_limite_retirada = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Aguardando'
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='ID_usuario'
    )

    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        db_column='ID_livro'
    )

    def __str__(self):
        return f'Reserva {self.id_reserva} - {self.livro.titulo}'

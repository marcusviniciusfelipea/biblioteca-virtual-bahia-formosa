from django.db import models
from livros.models import Livro


class Exemplar(models.Model):
    id_exemplar = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    autor = models.CharField(max_length=60)

    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        db_column='ID_livro'
    )

    def __str__(self):
        return f'{self.titulo} - Exemplar {self.id_exemplar}'
    
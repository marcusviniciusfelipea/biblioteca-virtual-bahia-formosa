from django.db import models


class Livro(models.Model):
    id_livro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    autor = models.CharField(max_length=60)

    def __str__(self):
        return self.titulo
    
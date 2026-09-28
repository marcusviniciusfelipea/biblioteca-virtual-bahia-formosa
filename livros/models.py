from django.db import models


class Livro(models.Model):
    id_livro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    autor = models.CharField(max_length=60)
    imagem = models.ImageField(upload_to='livros/', blank=True, null=True)
    sinopse = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo
    
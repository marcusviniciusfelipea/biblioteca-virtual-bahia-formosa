from django.shortcuts import render
from django.db.models import Q

from livros.models import Livro
from exemplares.models import Exemplar
from usuarios.models import Usuario


def inicio(request):
    busca = request.GET.get('q', '').strip()

    livros = Livro.objects.all()

    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca) |
            Q(autor__icontains=busca)
        )

    return render(request, 'index.html', {
        'livros': livros,
        'busca': busca,
    })


def cadastro(request):
    return render(request, 'cadastro.html')
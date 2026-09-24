from django.shortcuts import render, redirect
from django.db.models import Q

from livros.models import Livro
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

    if request.method == 'POST':

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')

        Usuario.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senha
        )

        return redirect('inicio')

    return render(request, 'cadastro.html')


def catalogo(request):
    busca = request.GET.get('q', '').strip()

    livros = Livro.objects.all()

    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca) |
            Q(autor__icontains=busca)
        )

    return render(request, 'catalogo.html', {
        'livros': livros,
        'busca': busca,
    })


def servicos(request):
    return render(request, 'servicos.html')


def contato(request):
    return render(request, 'contato.html')
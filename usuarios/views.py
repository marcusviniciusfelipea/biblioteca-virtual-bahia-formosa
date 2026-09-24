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

    usuario = None

    if request.session.get('usuario_id'):
        usuario = Usuario.objects.filter(
            id_usuario=request.session['usuario_id']
        ).first()

    return render(request, 'index.html', {
        'livros': livros,
        'busca': busca,
        'usuario': usuario,
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

def login(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario.objects.filter(
            email=email,
            senha=senha
        ).first()

        if usuario:
            request.session['usuario_id'] = usuario.id_usuario
            return redirect('inicio')

        return render(request, 'login.html', {
            'erro': 'E-mail ou senha incorretos.'
        })

    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('inicio')
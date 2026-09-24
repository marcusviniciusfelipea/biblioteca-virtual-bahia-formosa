from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone

from livros.models import Livro
from usuarios.models import Usuario
from exemplares.models import Exemplar
from emprestimos.models import Emprestimo


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

    hoje = timezone.now().date()

    livros_com_exemplares = []

    for livro in livros:

        exemplares = Exemplar.objects.filter(
            livro=livro
        )

        quantidade_exemplares = exemplares.count()

        quantidade_emprestados = Emprestimo.objects.filter(
            exemplar__in=exemplares,
            previsao_devolucao__gte=hoje
        ).count()

        quantidade_disponiveis = (
            quantidade_exemplares - quantidade_emprestados
        )

        if quantidade_exemplares == 0:
            status = 'Sem exemplares'

        elif quantidade_disponiveis > 0:
            status = 'Disponível'

        else:
            status = 'Indisponível'

        livros_com_exemplares.append({
            'livro': livro,
            'quantidade_exemplares': quantidade_exemplares,
            'quantidade_disponiveis': quantidade_disponiveis,
            'status': status,
        })

    return render(request, 'catalogo.html', {
        'livros': livros_com_exemplares,
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

def minha_conta(request):

    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario = Usuario.objects.filter(
        id_usuario=request.session['usuario_id']
    ).first()

    return render(request, 'minha_conta.html', {
        'usuario': usuario,
    })

def detalhes_livro(request, id_livro):

    livro = Livro.objects.filter(
        id_livro=id_livro
    ).first()

    if not livro:
        return redirect('catalogo')

    exemplares = Exemplar.objects.filter(
        livro=livro
    )

    return render(request, 'detalhes_livro.html', {
        'livro': livro,
        'exemplares': exemplares,
    })
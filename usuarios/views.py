from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

from livros.models import Livro
from usuarios.models import Usuario
from funcionarios.models import Funcionario
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
    funcionario = None

    if request.session.get('usuario_id'):
        usuario = Usuario.objects.filter(
        id_usuario=request.session['usuario_id']
    ).first()

    if request.session.get('funcionario_id'):
        funcionario = Funcionario.objects.filter(
        id_funcionario=request.session['funcionario_id']
    ).first()

    return render(request, 'index.html', {
        'livros': livros,
        'busca': busca,
        'usuario': usuario,
        'funcionario': funcionario,
})


def cadastro(request):

    if request.method == 'POST':

        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        senha = request.POST.get('senha', '').strip()

        erros = []

        # Verifica se os campos foram preenchidos
        if not nome:
            erros.append('O nome é obrigatório.')

        if not email:
            erros.append('O e-mail é obrigatório.')

        if not telefone:
            erros.append('O telefone é obrigatório.')

        if not senha:
            erros.append('A senha é obrigatória.')

        # Verifica o formato do e-mail
        if email:
            try:
                validate_email(email)
            except ValidationError:
                erros.append('Digite um e-mail válido.')

        # Verifica se o e-mail já está cadastrado
        if email and Usuario.objects.filter(email=email).exists():
            erros.append('Este e-mail já está cadastrado.')

        # Verifica o telefone
        if telefone:
            numeros_telefone = re.sub(r'\D', '', telefone)

            if len(numeros_telefone) != 11:
                erros.append(
                    'Digite um telefone válido com DDD e 9 dígitos.'
                )

        # Verifica o tamanho da senha
        if senha and len(senha) < 6:
            erros.append('A senha deve ter pelo menos 6 caracteres.')

        # Se houver algum erro, volta para o cadastro
        if erros:
            return render(request, 'cadastro.html', {
                'erros': erros,
                'nome': nome,
                'email': email,
                'telefone': telefone,
            })

        # Se estiver tudo certo, cria o usuário
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

        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        erros = []

        # Verifica se os campos foram preenchidos
        if not email:
            erros.append('O e-mail é obrigatório.')

        if not senha:
            erros.append('A senha é obrigatória.')

        # Verifica o formato do e-mail
        if email:
            try:
                validate_email(email)
            except ValidationError:
                erros.append('Digite um e-mail válido.')

        # Se houver algum erro, volta para o login
        if erros:
            return render(request, 'login.html', {
                'erros': erros,
                'email': email,
            })

        # Procura o usuário
        usuario = Usuario.objects.filter(
            email=email,
            senha=senha
        ).first()

        if usuario:
            request.session.pop('funcionario_id', None)
            request.session['usuario_id'] = usuario.id_usuario
            return redirect('inicio')

        # E-mail ou senha não correspondem
        return render(request, 'login.html', {
            'erros': ['E-mail ou senha incorretos.'],
            'email': email,
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

    hoje = timezone.now().date()

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

    return render(request, 'detalhes_livro.html', {
        'livro': livro,
        'exemplares': exemplares,
        'quantidade_exemplares': quantidade_exemplares,
        'quantidade_disponiveis': quantidade_disponiveis,
        'status': status,
    })


def bibliotecario_login(request):

    if request.method == 'POST':

        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '').strip()

        erros = []

        # Verifica se os campos foram preenchidos
        if not email:
            erros.append('O e-mail é obrigatório.')

        if not senha:
            erros.append('A senha é obrigatória.')

        # Verifica o formato do e-mail
        if email:
            try:
                validate_email(email)
            except ValidationError:
                erros.append('Digite um e-mail válido.')

        # Se houver algum erro, volta para o login
        if erros:
            return render(request, 'bibliotecario_login.html', {
                'erros': erros,
                'email': email,
                'usuario': None,
                'funcionario': None,
            })

        # Procura o funcionário
        funcionario = Funcionario.objects.filter(
            email=email,
            senha=senha
        ).first()

        if funcionario:
            # Remove o usuário comum da sessão
            request.session.pop('usuario_id', None)

            # Salva o funcionário na sessão
            request.session['funcionario_id'] = funcionario.id_funcionario

            return redirect('inicio')

        # Login incorreto
        return render(request, 'bibliotecario_login.html', {
            'erros': ['E-mail ou senha incorretos.'],
            'email': email,
            'usuario': None,
            'funcionario': None,
        })

    return render(request, 'bibliotecario_login.html', {
        'usuario': None,
        'funcionario': None,
    })
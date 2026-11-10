
from datetime import timedelta

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Emprestimo
from usuarios.models import Usuario
from funcionarios.models import Funcionario
from exemplares.models import Exemplar
from prazo.models import Prazo
from reservas.models import Reserva


def gerenciar_emprestimos(request):

    if not request.session.get('funcionario_id'):
        return redirect('bibliotecario_login')

    funcionario = Funcionario.objects.filter(
        id_funcionario=request.session['funcionario_id']
    ).first()

    if not funcionario:
        request.session.flush()
        return redirect('bibliotecario_login')

    if request.method == 'POST':

        usuario_id = request.POST.get('usuario')
        exemplar_id = request.POST.get('exemplar')

        usuario = get_object_or_404(
            Usuario,
            id_usuario=usuario_id
        )

        with transaction.atomic():

            exemplar = get_object_or_404(
                Exemplar.objects.select_for_update(),
                id_exemplar=exemplar_id
            )

            emprestimo_ativo = Emprestimo.objects.filter(
                exemplar=exemplar,
                data_devolucao__isnull=True
            ).exists()

            if emprestimo_ativo:
                messages.error(
                    request,
                    'Este exemplar já está emprestado.'
                )
                return redirect('gerenciar_emprestimos')

            # Verifica a primeira reserva ativa deste livro.
            primeira_reserva = Reserva.objects.select_for_update().filter(
                livro=exemplar.livro,
                status__in=['Aguardando', 'Disponível']
            ).order_by('id_reserva').first()

            # Se existe reserva, verifica se pode ser retirada
            # e se pertence ao usuário selecionado.
            if primeira_reserva:

                if primeira_reserva.status != 'Disponível':
                    messages.error(
                        request,
                        'Este livro ainda não está disponível para retirada.'
                    )
                    return redirect('gerenciar_emprestimos')

                if primeira_reserva.usuario_id != usuario.id_usuario:
                    messages.error(
                        request,
                        f'Este livro está reservado para {primeira_reserva.usuario.nome}.'
                    )
                    return redirect('gerenciar_emprestimos')

            prazo = Prazo.objects.first()

            if not prazo:
                messages.error(
                    request,
                    'Cadastre uma configuração de prazo antes de registrar empréstimos.'
                )
                return redirect('gerenciar_emprestimos')

            data_emprestimo = timezone.localdate()
            previsao = data_emprestimo + timedelta(days=7)

            Emprestimo.objects.create(
                data=data_emprestimo,
                previsao_devolucao=previsao,
                exemplar=exemplar,
                usuario=usuario,
                prazo=prazo
            )

            # Conclui a reserva quando o empréstimo é feito
            # para a pessoa que está no início da fila.
            if primeira_reserva:
                primeira_reserva.status = 'Concluída'
                primeira_reserva.save(update_fields=['status'])

        messages.success(
            request,
            f'Empréstimo registrado! Devolução prevista para '
            f'{previsao.strftime("%d/%m/%Y")}.'
        )

        return redirect('gerenciar_emprestimos')

    emprestimos = Emprestimo.objects.select_related(
        'usuario',
        'exemplar',
        'exemplar__livro'
    ).order_by('-data')

    usuarios = Usuario.objects.all().order_by('nome')

    emprestimos_ativos = Emprestimo.objects.filter(
        data_devolucao__isnull=True
    ).values_list('exemplar_id', flat=True)

    exemplares = Exemplar.objects.exclude(
        id_exemplar__in=emprestimos_ativos
    ).select_related('livro').order_by('livro__titulo')

    return render(request, 'gerenciar_emprestimos.html', {
        'funcionario': funcionario,
        'emprestimos': emprestimos,
        'usuarios': usuarios,
        'exemplares': exemplares,
    })


def gerenciar_devolucoes(request):

    if not request.session.get('funcionario_id'):
        return redirect('bibliotecario_login')

    funcionario = Funcionario.objects.filter(
        id_funcionario=request.session['funcionario_id']
    ).first()

    if not funcionario:
        request.session.flush()
        return redirect('bibliotecario_login')

    emprestimos = Emprestimo.objects.filter(
        data_devolucao__isnull=True
    ).select_related(
        'usuario',
        'exemplar',
        'exemplar__livro'
    ).order_by('previsao_devolucao')

    return render(request, 'gerenciar_devolucoes.html', {
        'funcionario': funcionario,
        'emprestimos': emprestimos,
    })


def registrar_devolucao(request, emprestimo_id):

    if not request.session.get('funcionario_id'):
        return redirect('bibliotecario_login')

    if request.method != 'POST':
        return redirect('gerenciar_emprestimos')

    emprestimo = get_object_or_404(
        Emprestimo,
        id=emprestimo_id
    )

    if emprestimo.data_devolucao:

        messages.info(
            request,
            'Este livro já foi devolvido.'
        )

    else:

        emprestimo.data_devolucao = timezone.localdate()

        emprestimo.save(
            update_fields=['data_devolucao']
        )

        livro = emprestimo.exemplar.livro

        # Busca a primeira reserva que está aguardando.
        reserva = Reserva.objects.filter(
            livro=livro,
            status='Aguardando'
        ).order_by('id_reserva').first()

        # Só atualiza a data se realmente existir uma reserva.
        if reserva:

            reserva.status = 'Disponível'

            reserva.data_limite_retirada = (
                timezone.localdate() + timedelta(days=3)
            )

            reserva.save(
                update_fields=[
                    'status',
                    'data_limite_retirada'
                ]
            )

            messages.info(
                request,
                f'O livro ficou disponível para {reserva.usuario.nome}.'
            )

        messages.success(
            request,
            f'Devolução de "{livro.titulo}" registrada.'
        )

    return redirect('gerenciar_emprestimos')

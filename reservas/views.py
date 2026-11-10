
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from .models import Reserva
from livros.models import Livro
from usuarios.models import Usuario
from exemplares.models import Exemplar
from emprestimos.models import Emprestimo




def reservar_livro(request, id_livro):

    if not request.session.get('usuario_id'):
        messages.warning(
            request,
            'Faça login para reservar um livro.'
        )
        return redirect('login')

    if request.method != 'POST':
        return redirect('detalhes_livro', id_livro=id_livro)

    usuario = get_object_or_404(
        Usuario,
        id_usuario=request.session['usuario_id']
    )

    with transaction.atomic():

        livro = get_object_or_404(
            Livro.objects.select_for_update(),
            id_livro=id_livro
        )

        exemplares = Exemplar.objects.filter(livro=livro)

        if not exemplares.exists():
            messages.error(
                request,
                'Este livro ainda não possui exemplares cadastrados e não pode ser reservado.'
            )
            return redirect('detalhes_livro', id_livro=id_livro)

        reserva_existente = Reserva.objects.filter(
            usuario=usuario,
            livro=livro,
            status__in=['Aguardando', 'Disponível']
        ).exists()

        if reserva_existente:
            messages.warning(
                request,
                'Você já possui uma reserva ativa para este livro.'
            )
            return redirect('detalhes_livro', id_livro=id_livro)

        quantidade_emprestada = Emprestimo.objects.filter(
            exemplar__in=exemplares,
            data_devolucao__isnull=True
        ).count()

        quantidade_reservada = Reserva.objects.filter(
            livro=livro,
            status='Disponível'
        ).count()

        quantidade_disponivel = (
            exemplares.count()
            - quantidade_emprestada
            - quantidade_reservada
        )

        existe_fila = Reserva.objects.filter(
            livro=livro,
            status='Aguardando'
        ).exists()

        if quantidade_disponivel > 0:
            status = 'Disponível'
            data_limite = timezone.localdate() + timedelta(days=3)
        else:
            status = 'Aguardando'
            data_limite = None

        Reserva.objects.create(
            usuario=usuario,
            livro=livro,
            status=status,
            data_limite_retirada=data_limite
        )

    if status == 'Disponível':
        messages.success(
            request,
            'Sua reserva foi registrada! O livro está disponível para retirada.'
        )
    else:
        messages.success(
            request,
            'Sua reserva foi registrada! Você entrou na fila de espera.'
        )

    return redirect('detalhes_livro', id_livro=id_livro)


def cancelar_reserva(request, id_reserva):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario = get_object_or_404(
        Usuario,
        id_usuario=request.session['usuario_id']
    )

    reserva = get_object_or_404(
        Reserva,
        id_reserva=id_reserva,
        usuario=usuario
    )

    if reserva.status not in ['Aguardando', 'Disponível']:
        messages.warning(
            request,
            'Esta reserva não pode mais ser cancelada.'
        )
        return redirect('minha_conta')

    if request.method == 'POST':
        reserva.status = 'Cancelada'
        reserva.save(update_fields=['status'])

        messages.success(request, 'Reserva cancelada com sucesso!')
        return redirect('minha_conta')

    return render(request, 'confirmar_cancelamento_reserva.html', {
        'reserva': reserva,
    })

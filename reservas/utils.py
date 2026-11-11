
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import Reserva


def atualizar_reservas_vencidas():

    hoje = timezone.localdate()

    with transaction.atomic():

        reservas_vencidas = Reserva.objects.select_for_update().filter(
            status='Disponível',
            data_limite_retirada__lt=hoje
        ).order_by('id_reserva')

        for reserva in reservas_vencidas:

            livro_id = reserva.livro_id

            reserva.status = 'Cancelada'
            reserva.save(update_fields=['status'])

            proxima_reserva = Reserva.objects.select_for_update().filter(
                livro_id=livro_id,
                status='Aguardando'
            ).order_by('id_reserva').first()

            if proxima_reserva:

                proxima_reserva.status = 'Disponível'

                proxima_reserva.data_limite_retirada = (
                    hoje + timedelta(days=3)
                )

                proxima_reserva.save(
                    update_fields=[
                        'status',
                        'data_limite_retirada'
                    ]
                )

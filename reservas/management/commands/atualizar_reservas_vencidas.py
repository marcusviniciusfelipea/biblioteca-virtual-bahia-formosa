
from django.core.management.base import BaseCommand
from reservas.utils import atualizar_reservas_vencidas


class Command(BaseCommand):
    help = 'Verifica reservas vencidas e libera a próxima da fila.'

    def handle(self, *args, **options):
        atualizar_reservas_vencidas()

        self.stdout.write(
            self.style.SUCCESS(
                'Verificação de reservas concluída com sucesso.'
            )
        )

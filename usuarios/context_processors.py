from .models import Usuario
from funcionarios.models import Funcionario


def dados_usuario(request):

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

    return {
        'usuario': usuario,
        'funcionario': funcionario,
    }
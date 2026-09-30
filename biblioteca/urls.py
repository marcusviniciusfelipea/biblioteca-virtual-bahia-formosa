from django.contrib import admin
from django.urls import path
from usuarios import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', views.inicio, name='inicio'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path(
    'bibliotecario/login/',
    views.bibliotecario_login,
    name='bibliotecario_login'
),
    path(
    'bibliotecario/',
    views.painel_funcionario,
    name='painel_funcionario'
),
    path(
    'bibliotecario/livros/',
    views.gerenciar_livros,
    name='gerenciar_livros'
),
    path(
    'bibliotecario/livros/<int:id_livro>/editar/',
    views.editar_livro,
    name='editar_livro'
),
    path(
    'bibliotecario/livros/<int:id_livro>/excluir/',
    views.excluir_livro,
    name='excluir_livro'
),
    path('minha-conta/', views.minha_conta, name='minha_conta'),

    path('catalogo/', views.catalogo, name='catalogo'),

    path(
        'livro/<int:id_livro>/',
        views.detalhes_livro,
        name='detalhes_livro'
    ),

    path('servicos/', views.servicos, name='servicos'),
    path('contato/', views.contato, name='contato'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

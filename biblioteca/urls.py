from django.contrib import admin
from django.urls import path
from usuarios import views

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
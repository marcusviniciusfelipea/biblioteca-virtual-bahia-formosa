from django.contrib import admin
from django.urls import path
from usuarios import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', views.inicio, name='inicio'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),

    path('catalogo/', views.catalogo, name='catalogo'),
    path('servicos/', views.servicos, name='servicos'),
    path('contato/', views.contato, name='contato'),
    path('logout/', views.logout, name='logout'),
]
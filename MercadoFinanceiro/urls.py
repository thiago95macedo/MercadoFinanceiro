# Importações
from django.contrib import admin  # Importa o módulo de administração do Django
from django.urls import path  # Importa a função path para definir as rotas
from django.shortcuts import redirect  # Importa a função redirect para redirecionar as requisições

# Função de Redirecionamento para Admin
def redirect_to_admin(request):  # Define uma função de view que redireciona para /admin
    return redirect('/admin')  # Retorna um redirecionamento para /admin

# Definição das Rotas
urlpatterns = [
    path('admin/', admin.site.urls),  # Define a rota para a interface de administração do Django
    path('', redirect_to_admin),  # Define a rota raiz para redirecionar para /admin
]
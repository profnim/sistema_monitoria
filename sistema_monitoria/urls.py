from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from monitorias import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monitorias.urls')),
    # Rotas padrão de login/logout do Django
    path('accounts/login/', auth_views.LoginView.as_view(template_name='monitorias/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
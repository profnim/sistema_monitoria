from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_monitorias, name='lista_monitorias'),
    path('inscrever/<int:monitoria_id>/', views.inscrever_monitoria, name='inscrever_monitoria'),
    path('cancelar/<int:monitoria_id>/', views.cancelar_inscricao, name='cancelar_inscricao'),
    # Novas rotas do monitor
    path('painel-monitor/', views.painel_monitor, name='painel_monitor'),
    path('gerenciar/<int:monitoria_id>/', views.gerenciar_monitoria, name='gerenciar_monitoria'),
    
    path('painel-admin/', views.painel_admin, name='painel_admin'),
path('painel-admin/nova-monitoria/', views.criar_monitoria, name='criar_monitoria'),
path('painel-admin/excluir/<int:monitoria_id>/', views.excluir_monitoria, name='excluir_monitoria'),
path('painel-admin/editar/<int:monitoria_id>/', views.editar_monitoria, name='editar_monitoria'),
]
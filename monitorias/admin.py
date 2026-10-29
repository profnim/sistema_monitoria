from django.contrib import admin
from .models import Monitoria, HorarioMonitoria, Inscricao

# Opcional: Permite cadastrar os horários diretamente dentro da tela da Monitoria no Admin
class HorarioMonitoriaInline(admin.TabularInline):
    model = HorarioMonitoria
    extra = 1

@admin.register(Monitoria)
class MonitoriaAdmin(admin.ModelAdmin):
    # Removemos 'data' e 'horario_inicio' daqui, pois agora ficam no HorarioMonitoria
    list_display = ('disciplina', 'assunto', 'monitor', 'local', 'vagas_limite')
    search_fields = ('disciplina', 'assunto')
    inlines = [HorarioMonitoriaInline] # Permite gerenciar os horários direto na tela da monitoria

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('monitoria', 'aluno', 'data_inscricao', 'presente')
    list_filter = ('presente', 'data_inscricao')
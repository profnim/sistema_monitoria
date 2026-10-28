from django.contrib import admin
from .models import Monitoria, Inscricao

@admin.register(Monitoria)
class MonitoriaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'assunto', 'monitor', 'data', 'horario_inicio', 'vagas_limite')
    list_filter = ('data', 'disciplina')
    search_fields = ('disciplina', 'assunto', 'monitor__username')

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('monitoria', 'aluno', 'data_inscricao')
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Monitoria(models.Model):
    disciplina = models.CharField(max_length=100)
    assunto = models.CharField(max_length=200)
    monitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monitorias_ministradas')
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    local = models.CharField(max_length=100, default="Laboratório de Informática")
    vagas_limite = models.PositiveIntegerField(default=20)

    class Meta:
        ordering = ['data', 'horario_inicio']

    def vagas_disponiveis(self):
        return self.vagas_limite - self.inscricoes.count()

    def __str__(self):
        return f"{self.disciplina} - {self.assunto} ({self.data.strftime('%d/%m/%Y')})"


class Inscricao(models.Model):
    monitoria = models.ForeignKey(Monitoria, on_delete=models.CASCADE, related_name='inscricoes')
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='minhas_inscricoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    presente = models.BooleanField(default=False)

    class Meta:
        unique_together = ('monitoria', 'aluno')

    def __str__(self):
        return f"{self.aluno.username} - {self.monitoria.disciplina}"
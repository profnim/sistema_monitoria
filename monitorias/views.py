from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Monitoria, Inscricao
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.db import models
from .forms import CustomUserCreationForm

# Função para Cadastro de Usuários Comuns
def cadastrar_usuario(request):
    if request.user.is_authenticated:
        return redirect('lista_monitorias')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"Conta criada com sucesso! Bem-vindo(a), {usuario.username}!")
            return redirect('lista_monitorias')
    else:
        form = CustomUserCreationForm()

    return render(request, 'monitorias/cadastro.html', {'form': form})

@login_required
def lista_monitorias(request):
    hoje = timezone.localdate() # Pega a data de hoje
    busca = request.GET.get('q', '')
    
    # Exibe para o aluno apenas monitorias de hoje em diante
    monitorias = Monitoria.objects.filter(data__gte=hoje)

    # Filtro por busca de disciplina ou assunto
    if busca:
        monitorias = monitorias.filter(
            models.Q(disciplina__icontains=busca) | 
            models.Q(assunto__icontains=busca)
        )

    monitorias = monitorias.order_by('data')

    # Pega os IDs das monitorias em que o usuário atual já está inscrito
    inscricoes_usuario = Inscricao.objects.filter(aluno=request.user).values_list('monitoria_id', flat=True)
    
    context = {
        'monitorias': monitorias,
        'inscricoes_usuario': inscricoes_usuario,
        'busca': busca,
    }
    return render(request, 'monitorias/lista.html', context)


@login_required
def inscrever_monitoria(request, monitoria_id):
    monitoria = get_object_or_404(Monitoria, pk=monitoria_id)
    
    if monitoria.vagas_disponiveis() <= 0:
        messages.error(request, "Esta monitoria já atingiu o limite de vagas.")
        return redirect('lista_monitorias')

    _, created = Inscricao.objects.get_or_create(
        monitoria=monitoria, 
        aluno=request.user
    )

    if created:
        messages.success(request, f"Inscrição realizada com sucesso na monitoria de {monitoria.disciplina}!")
    else:
        messages.warning(request, "Você já está inscrito nesta monitoria.")

    return redirect('lista_monitorias')


@login_required
def cancelar_inscricao(request, monitoria_id):
    monitoria = get_object_or_404(Monitoria, pk=monitoria_id)
    Inscricao.objects.filter(monitoria=monitoria, aluno=request.user).delete()
    messages.info(request, "Inscrição cancelada com sucesso.")
    return redirect('lista_monitorias')


@login_required
def painel_monitor(request):
    e_monitor = Monitoria.objects.filter(monitor=request.user).exists()
    
    if not e_monitor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para acessar o Painel do Monitor.")
        return redirect('lista_monitorias')

    monitorias = Monitoria.objects.filter(monitor=request.user)
    return render(request, 'monitorias/painel_monitor.html', {'monitorias': monitorias})


@login_required
def gerenciar_monitoria(request, monitoria_id):
    monitoria = get_object_or_404(Monitoria, pk=monitoria_id)
    
    if monitoria.monitor != request.user and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para gerenciar esta monitoria.")
        return redirect('lista_monitorias')

    inscricoes = monitoria.inscricoes.all().order_by('aluno__username')

    if request.method == 'POST':
        presentes_ids = request.POST.getlist('presentes')
        for inscricao in inscricoes:
            inscricao.presente = str(inscricao.aluno.id) in presentes_ids
            inscricao.save()
            
        messages.success(request, "Lista de presença salva com sucesso!")
        return redirect('gerenciar_monitoria', monitoria_id=monitoria.id)

    context = {
        'monitoria': monitoria,
        'inscricoes': inscricoes
    }
    return render(request, 'monitorias/gerenciar_monitoria.html', context)


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "Acesso restrito a administradores.")
            return redirect('lista_monitorias')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def painel_admin(request):
    total_monitorias = Monitoria.objects.count()
    total_usuarios = User.objects.count()
    total_inscricoes = Inscricao.objects.count()
    
    # O Administrador vê TODAS as monitorias (passadas e futuras) para controle
    monitorias = Monitoria.objects.all().order_by('-data')
    
    context = {
        'total_monitorias': total_monitorias,
        'total_usuarios': total_usuarios,
        'total_inscricoes': total_inscricoes,
        'monitorias': monitorias,
    }
    return render(request, 'monitorias/painel_admin.html', context)


@login_required
@admin_required
def criar_monitoria(request):
    if request.method == 'POST':
        disciplina = request.POST.get('disciplina')
        assunto = request.POST.get('assunto')
        monitor_id = request.POST.get('monitor')
        data = request.POST.get('data')
        horario_inicio = request.POST.get('horario_inicio')
        horario_fim = request.POST.get('horario_fim')
        local = request.POST.get('local')
        vagas_limite = request.POST.get('vagas_limite')

        monitor = get_object_or_404(User, pk=monitor_id)

        Monitoria.objects.create(
            disciplina=disciplina,
            assunto=assunto,
            monitor=monitor,
            data=data,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            local=local,
            vagas_limite=vagas_limite
        )
        messages.success(request, "Monitoria cadastrada com sucesso!")
        return redirect('painel_admin')

    monitores = User.objects.filter(is_active=True)
    return render(request, 'monitorias/form_monitoria.html', {'monitores': monitores})


@login_required
@admin_required
def editar_monitoria(request, monitoria_id):
    monitoria = get_object_or_404(Monitoria, pk=monitoria_id)
    
    if request.method == 'POST':
        monitoria.disciplina = request.POST.get('disciplina')
        monitoria.assunto = request.POST.get('assunto')
        monitor_id = request.POST.get('monitor')
        monitoria.data = request.POST.get('data')
        monitoria.horario_inicio = request.POST.get('horario_inicio')
        monitoria.horario_fim = request.POST.get('horario_fim')
        monitoria.local = request.POST.get('local')
        monitoria.vagas_limite = request.POST.get('vagas_limite')

        monitoria.monitor = get_object_or_404(User, pk=monitor_id)
        monitoria.save()
        
        messages.success(request, "Monitoria atualizada com sucesso!")
        return redirect('painel_admin')

    monitores = User.objects.filter(is_active=True)
    context = {
        'monitoria': monitoria,
        'monitores': monitores,
        'editando': True
    }
    return render(request, 'monitorias/form_monitoria.html', context)


@login_required
@admin_required
def excluir_monitoria(request, monitoria_id):
    monitoria = get_object_or_404(Monitoria, pk=monitoria_id)
    monitoria.delete()
    messages.success(request, "Monitoria excluída com sucesso.")
    return redirect('painel_admin')
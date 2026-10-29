import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):  # <--- O nome DEVE ser Command com C maiúsculo
    help = 'Cria ou atualiza o superusuário automaticamente usando as variáveis de ambiente do Render'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'Admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@admin.com')
        password = os.environ.get('ADMIN_PASSWORD')

        if not password:
            self.stdout.write(self.style.WARNING('Aviso: ADMIN_PASSWORD não foi definida nas variáveis de ambiente.'))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso!'))
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Senha do usuário "{username}" atualizada com sucesso!'))
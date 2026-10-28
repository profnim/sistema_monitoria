
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_monitoria.settings")
django.setup()

from django.contrib.auth import get_user_model

Usuario = get_user_model()

nome = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
senha = os.environ.get("ADMIN_PASSWORD")

if not nome or not email or not senha:
    raise ValueError("Configure ADMIN_USERNAME, ADMIN_EMAIL e ADMIN_PASSWORD.")

usuario, criado = Usuario.objects.get_or_create(
    username=nome,
    defaults={"email": email, "is_staff": True, "is_superuser": True},
)

if not criado:
    usuario.is_staff = True
    usuario.is_superuser = True

usuario.email = email
usuario.set_password(senha)
usuario.save()

print("Administrador criado ou atualizado com sucesso.")

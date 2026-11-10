from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from usuarios.models import PerfilUsuario, Rol


class RegistroYAccesoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('configurar_roles')

    def test_portada_publica(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cada patita merece')

    def test_registro_crea_usuario_y_perfil(self):
        response = self.client.post(reverse('registro'), {
            'username': 'vecina', 'nombre': 'Persona Solidaria',
            'email': 'vecina@example.com', 'password1': 'LargaSeguraDemo!2026',
            'password2': 'LargaSeguraDemo!2026',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='vecina').exists())
        self.assertEqual(PerfilUsuario.objects.get(usuario__username='vecina').rol.nombre_rol, Rol.NombreRol.CIUDADANO)
        self.assertTrue(Group.objects.get(name='Ciudadano').user_set.filter(username='vecina').exists())

    def test_sin_permiso_no_puede_ver_usuarios(self):
        user = User.objects.create_user('persona', password='SeguraDemo!2026')
        self.client.force_login(user)
        response = self.client.get(reverse('usuarios:usuario_lista'))
        self.assertEqual(response.status_code, 403)

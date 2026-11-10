from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from reportes.models import Reporte
from usuarios.models import PerfilUsuario, Rol

class ReportesFlujoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('configurar_roles')
        cls.user = User.objects.create_user('vecino', password='SeguraDemo!2026')
        cls.user.groups.add(Group.objects.get(name='Ciudadano'))
        cls.perfil = PerfilUsuario.objects.create(usuario=cls.user, nombre='Vecino', correo='vecino@example.com', rol=Rol.objects.get(nombre_rol='Ciudadano'))

    def test_reporte_guardado_en_sqlite_por_usuario_autenticado(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('reportes:crear'), {
            'descripcion': 'Perrito mediano junto a la plaza',
            'ubicacion': 'Colonia Centro', 'prioridad': 'Media',
        })
        self.assertEqual(response.status_code, 302)
        reporte = Reporte.objects.get()
        self.assertEqual(reporte.usuario, self.perfil)
        self.assertEqual(reporte.estatus, 'Reportado')

    def test_un_no_autenticado_no_puede_crear_reportes(self):
        response = self.client.get(reverse('reportes:crear'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

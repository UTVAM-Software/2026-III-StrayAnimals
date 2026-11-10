from django.contrib.auth.models import Group, Permission, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from reportes.models import Reporte
from hogares_temporales.models import HogarTemporal
from adopciones.models import SolicitudAdopcion
from usuarios.models import PerfilUsuario, Rol


class TiposAccesoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("configurar_roles", verbosity=0)
        cls.lector = User.objects.create_user("lector", password="ContraDePrueba-2026", email="lector@example.com")
        cls.lector.groups.add(Group.objects.get(name="Solo lectura"))
        cls.perfil_lector = PerfilUsuario.objects.create(
            usuario=cls.lector, nombre="Persona lectora", correo="lector@example.com",
            rol=Rol.objects.get(nombre_rol="Solo lectura"),
        )
        cls.usuario = User.objects.create_user("persona", password="ContraDePrueba-2026", email="persona@example.com")
        cls.usuario.groups.add(Group.objects.get(name="Ciudadano"))
        cls.perfil_usuario = PerfilUsuario.objects.create(
            usuario=cls.usuario, nombre="Persona ciudadana", correo="persona@example.com",
            rol=Rol.objects.get(nombre_rol="Ciudadano"),
        )
        cls.superusuario = User.objects.create_superuser("admin_prueba", "admin@example.com", "ContraDePrueba-2026")
        cls.reporte = Reporte.objects.create(usuario=cls.perfil_usuario, descripcion="Perrito junto a una plaza", ubicacion="Colonia Centro")
        cls.hogar = HogarTemporal.objects.create(usuario=cls.perfil_usuario, capacidad=1, disponibilidad=True)
        cls.solicitud = SolicitudAdopcion.objects.create(reporte=cls.reporte, usuario_interesado=cls.perfil_usuario)

    def test_lector_puede_iniciar_sesion_y_ver_listados(self):
        self.assertTrue(self.client.login(username="lector", password="ContraDePrueba-2026"))
        for url in [reverse("inicio"), reverse("reportes:lista"), reverse("reportes:detalle", args=[self.reporte.pk]), reverse("hogares_temporales:lista"), reverse("adopciones:lista")]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
        self.assertContains(self.client.get(reverse("inicio")), "Solo lectura")
        # La información privada de otros solicitantes NO se debe mostrar.
        self.assertNotContains(self.client.get(reverse("adopciones:lista")), f"Solicitud #{self.solicitud.pk}")

    def test_grupo_solo_lectura_no_recibe_permiso_de_escritura(self):
        grupo = Group.objects.get(name="Solo lectura")
        self.assertTrue(grupo.permissions.filter(codename="view_reporte").exists())
        self.assertFalse(grupo.permissions.exclude(codename__startswith="view_").exists())

    def test_lector_no_puede_crear_editar_eliminar_ni_actualizar_perfil(self):
        self.client.force_login(self.lector)
        rutas = [
            reverse("reportes:crear"), reverse("reportes:editar", args=[self.reporte.pk]), reverse("reportes:eliminar", args=[self.reporte.pk]),
            reverse("hogares_temporales:crear"), reverse("hogares_temporales:editar", args=[self.hogar.pk]), reverse("hogares_temporales:eliminar", args=[self.hogar.pk]),
            reverse("adopciones:crear"), reverse("adopciones:editar", args=[self.solicitud.pk]), reverse("adopciones:eliminar", args=[self.solicitud.pk]),
        ]
        for ruta in rutas:
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(ruta).status_code, 403)
                self.assertEqual(self.client.post(ruta, {}).status_code, 403)
        self.assertEqual(self.client.post(reverse("mi_perfil"), {"nombre":"cambio", "correo":"lector@example.com"}).status_code, 403)
        self.assertFalse(Reporte.objects.filter(usuario=self.perfil_lector).exists())

    def test_lector_no_puede_escribir_incluso_con_permiso_directo(self):
        permiso = Permission.objects.get(content_type__app_label="reportes", codename="add_reporte")
        self.lector.user_permissions.add(permiso)
        self.client.force_login(self.lector)
        self.assertEqual(self.client.post(reverse("reportes:crear"), {"descripcion":"nuevo", "ubicacion":"Centro"}).status_code, 403)

    def test_lector_puede_cerrar_sesion(self):
        self.client.force_login(self.lector)
        self.assertEqual(self.client.post(reverse("logout")).status_code, 302)

    def test_usuario_puede_publicar_reporte_pero_no_gestionar_usuarios(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(reverse("reportes:crear"), {"descripcion":"Perrito en parque", "ubicacion":"Centro", "prioridad":"Baja"})
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Reporte.objects.filter(descripcion="Perrito en parque").exists())
        self.assertEqual(self.client.get(reverse("usuarios:usuario_lista")).status_code, 403)

    def test_superusuario_puede_entrar_en_administracion_y_crud(self):
        self.client.force_login(self.superusuario)
        for ruta in [reverse("admin:index"),reverse("usuarios:usuario_lista"),reverse("reportes:crear"),reverse("adopciones:crear")]:
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(ruta).status_code, 200)

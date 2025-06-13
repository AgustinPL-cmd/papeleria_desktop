import flet as ft

from papeleria_app.models.usuario import Usuario


def empleado_dashboard_view():
    usuario = page.session.get("usuario", None)
    nombre = usuario.nombre if usuario else "Invitado"


    button = ft.ElevatedButton(nombre)
    return ft.View(
        route="/login",
        controls=[button],
        bgcolor="#cdf33ff",
        padding=0,
        appbar=None
    )
import flet as ft


def admin_dashboard_view(page):
    usuario_data = page.client_storage.get("usuario")
    if usuario_data:
        nombre = usuario_data["nombre"]
        rol = usuario_data["rol"]
    button = ft.ElevatedButton(nombre)

    return ft.View(
        route="/login",
        controls=[button],
        bgcolor="#cdf33ff",
        padding=0,
        appbar=None
    )
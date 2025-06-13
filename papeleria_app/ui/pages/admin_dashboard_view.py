import flet as ft


def admin_dashboard_view(page):
    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]
    button = ft.ElevatedButton(user)

    return ft.View(
        route="/login",
        controls=[button],
        bgcolor="#cdf33ff",
        padding=0,
        appbar=None
    )
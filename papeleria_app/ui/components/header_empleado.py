import flet as ft
from papeleria_app.ui.components.alert_perfil_info import alert_usuario_info

def header_empleado(user, page, dlg_usuario):
    def mostrar_dialogo(e=None):
        print("Abriendo el perfil")

        # Obtener el diálogo armado
        dlg_detalle = alert_usuario_info(page)
        dlg_usuario.title = dlg_detalle.title
        dlg_usuario.content = dlg_detalle.content
        dlg_usuario.bgcolor = dlg_detalle.bgcolor
        dlg_usuario.actions = [
            ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo())
        ]

        dlg_usuario.open = True
        page.update()

    def cerrar_dialogo():
        dlg_usuario.open = False
        page.update()

    def cerrar_sesion(e):
        page.client_storage.clear()
        page.go("/login")

    mensaje_bienvenida = ft.Text(
        value=f"Bienvenido {user['nombre']}",
        weight=ft.FontWeight.BOLD,
        size=18,
        color="#231f20"
    )

    perfil_button = ft.IconButton(
        icon=ft.Icons.PERSON_ROUNDED,
        bgcolor="#231f20",
        icon_color="#cdf3ff",
        hover_color="#626bbb",
        icon_size=32,
        width=60,
        height=60,
        style=ft.ButtonStyle(padding=10),
        tooltip="PERFIL",
        on_click=mostrar_dialogo
    )

    logout_button = ft.IconButton(
        icon=ft.Icons.LOGOUT,
        bgcolor="#231f20",
        icon_color="#ffb3b3",
        hover_color="#d32f2f",
        icon_size=32,
        width=60,
        height=60,
        tooltip="CERRAR SESIÓN",
        on_click=cerrar_sesion
    )

    return ft.Container(
        content=ft.Row(
            controls=[mensaje_bienvenida, ft.Row(controls=[perfil_button, logout_button], spacing=10)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#8285a2",
        height=90,
        padding=ft.padding.symmetric(horizontal=20),
    )

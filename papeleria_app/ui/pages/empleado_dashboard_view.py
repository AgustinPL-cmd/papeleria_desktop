import flet as ft
from papeleria_app.ui.components.container_form import Container_form


def empleado_dashboard_view(page):
    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]

    mensaje_bienvenida = ft.Text(
        f"Bienvenido {user['nombre']}",
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
        style=ft.ButtonStyle(padding=10)
    )

    # Botones del menú lateral
    home_button = ft.IconButton(icon=ft.Icons.HOME, bgcolor="#231f20", icon_color="#cdf3ff", hover_color="#626bbb", icon_size=32)
    vender_button = ft.IconButton(icon=ft.Icons.ATTACH_MONEY, bgcolor="#231f20", icon_color="#cdf3ff", hover_color="#626bbb", icon_size=32)
    comment_button = ft.IconButton(icon=ft.Icons.QUESTION_ANSWER, bgcolor="#231f20", icon_color="#cdf3ff", hover_color="#626bbb", icon_size=32)

    # Estado para el menú desplegable
    menu_expandido = ft.Ref[ft.Container]()

    def toggle_menu(e):
        menu_expandido.current.visible = not menu_expandido.current.visible
        page.update()

    # Botón para mostrar/ocultar menú
    toggle_menu_button = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_color="#ffffff",
        on_click=toggle_menu
    )

    # Header con fondo que se "respeta"
    header = ft.Container(
        content=ft.Row(
            controls=[
                toggle_menu_button,
                mensaje_bienvenida,
                perfil_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        bgcolor="#8285a2",
        height=90,
        padding=ft.padding.symmetric(horizontal=20),
    )

    # Menú lateral desplegable
    menu_lateral = ft.Container(
        ref=menu_expandido,
        content=ft.Column(
            controls=[home_button, vender_button, comment_button],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        bgcolor="#8e7db4",
        width=80,
        padding=20,
        visible=True,  # Visible al inicio
    )

    # Contenido principal (lo que queda al lado del menú)
    contenido_principal = ft.Container(
        content=ft.Column(
            controls=[header, ft.Text("Contenido principal aquí...")],
            expand=True
        ),
        expand=True,
        padding=20
    )

    # Layout general: Fila con menú lateral y contenido
    layout = ft.Row(
        controls=[
            menu_lateral,
            contenido_principal
        ],
        expand=True
    )

    return ft.View(
        route="/empleadoDashboard",
        controls=[layout],
        bgcolor="#cdf3ff",
        padding=0,
        appbar=None
    )


def main(page: ft.Page):
    page.window_maximized = True
    page.route = "/empleadoDashboard"
    page.views.append(empleado_dashboard_view(page))
    page.update()
    page.go(page.route)


ft.app(target=main)

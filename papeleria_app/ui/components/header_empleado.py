import flet as ft

def header_empleado(user):

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
        tooltip="PERFIL"
    )
    header = ft.Container(
            content=ft.Row(
                controls=[
                    mensaje_bienvenida,
                    perfil_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#8285a2",
            height=90,
            padding=ft.padding.symmetric(horizontal=20),
        )
    return header
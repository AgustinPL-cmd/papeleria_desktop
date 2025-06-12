import flet as ft


def inicio_view():
    logo = ft.Image(src="images/logo_blanco.jpg", width=200, height=200)

    layout = ft.Column(
        controls=[
            logo,
            ft.ElevatedButton("Ingresar", width=200, on_click=lambda e: e.page.go("/login")),
        ],
        spacing=40,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route="/",
        controls=[layout],
        bgcolor="#cdf3ff",
        padding=0,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=None

    )

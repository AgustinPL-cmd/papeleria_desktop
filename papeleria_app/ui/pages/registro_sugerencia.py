import flet as ft
from papeleria_app.ui.components.logo_header import Logo_header
from papeleria_app.models.sugerencia_cliente import SugerenciaCliente

from papeleria_app.repositorios.sugerencia_repo import insert_sugerencia


def registro_sugerencia_view(page: ft.Page):
    header = Logo_header("images/logo_blanco.jpg").getHeader()

    # Entradas
    producto_input = ft.TextField(label="PRODUCTO SUGERIDO", width=300)
    comentario_input = ft.TextField(label="COMENTARIO", multiline=True, max_lines=3, width=300)

    mensaje = ft.Text("", color="red", size=14, text_align=ft.TextAlign.CENTER)

    def registrar(e):
        sugerencia = SugerenciaCliente(
            producto_sugerido=producto_input.value,
            comentario=comentario_input.value
        )
        exito, msj = insert_sugerencia(sugerencia)
        mensaje.value = msj
        mensaje.color = "green" if exito else "red"
        page.update()

    def limpiar(e):
        producto_input.value = ""
        comentario_input.value = ""
        mensaje.value = ""
        page.update()

    form_container = ft.Container(
        width=500,
        height=500,
        padding=30,
        border_radius=20,
        bgcolor="#d8d5eb",
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            blur_radius=25,
            color="#aaa",
            spread_radius=1,
            offset=ft.Offset(3, 6)
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Text("SUGERENCIAS DE CLIENTES", size=22, weight="bold", color="black"),
                producto_input,
                comentario_input,
                mensaje,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Container(
                            content=ft.ElevatedButton("GUARDAR", on_click=registrar),
                            width=140,
                            border_radius=30,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=["#cfd8dc", "#90a4ae"]
                            ),
                            shadow=ft.BoxShadow(blur_radius=10, color="#888")
                        ),
                        ft.Container(
                            content=ft.ElevatedButton("LIMPIAR", on_click=limpiar),
                            width=140,
                            border_radius=30,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=["#cfd8dc", "#90a4ae"]
                            ),
                            shadow=ft.BoxShadow(blur_radius=10, color="#888")
                        )
                    ]
                )
            ]
        )
    )

    layout = ft.Column(
        expand=True,
        spacing=0,
        controls=[
            header,
            ft.Container(
                expand=True,
                bgcolor="#cdf3ff",
                alignment=ft.alignment.center,
                padding=0,
                margin=0,
                content=form_container
            )
        ]
    )

    return layout


def main(page: ft.Page):
    page.title = "Sugerencias"
    page.bgcolor = "#cdf3ff"
    page.views.clear()
    page.views.append(
        ft.View(
            route="/registro_sugerencia",
            bgcolor="#cdf3ff",
            padding=0,
            spacing=0,
            controls=[registro_sugerencia_view(page)],
        )
    )
    page.update()


ft.app(target=main)

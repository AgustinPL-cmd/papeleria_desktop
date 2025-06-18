import flet as ft
from papeleria_app.models.sugerencia_cliente import SugerenciaCliente
from papeleria_app.repositorios.sugerencia_repo import obtener_sugerencias, eliminar_sugerencia

estado_realizadas = {}

def sugerencias_view(page: ft.Page):
    tabla = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def marcar_como_realizada(id_sugerencia):
        estado_realizadas[id_sugerencia] = True
        actualizar_tabla()

    def eliminar(id_sugerencia):
        eliminar_sugerencia(id_sugerencia)
        estado_realizadas.pop(id_sugerencia, None)
        actualizar_tabla()

    def crear_fila(sugerencia: SugerenciaCliente):
        realizada = estado_realizadas.get(sugerencia.id_sugerencia, False)
        fila_color = "#e8f5e9" if realizada else "#ffffff"
        border_color = "#c8e6c9" if realizada else "#e0e0e0"

        boton_check = ft.IconButton(
            icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
            icon_color="#2e7d32",
            tooltip="Marcar como realizada",
            visible=not realizada,
            on_click=lambda e: marcar_como_realizada(sugerencia.id_sugerencia)
        )

        fila = ft.Container(
            bgcolor=fila_color,
            padding=10,
            border=ft.border.all(1, border_color),
            border_radius=8,
            margin=ft.margin.only(bottom=5),
            content=ft.Row([
                ft.Container(
                    content=ft.Text(
                        sugerencia.fecha_sugerencia.strftime("%d/%m/%Y"),
                        color=ft.Colors.GREY_800
                    ),
                    width=120,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Text(
                        sugerencia.producto_sugerido,
                        color=ft.Colors.GREY_800,
                        weight=ft.FontWeight.W_500
                    ),
                    width=200,
                    padding=5
                ),
                ft.Container(
                    content=ft.Text(
                        sugerencia.comentario,
                        color=ft.Colors.GREY_800
                    ),
                    width=300,
                    padding=5
                ),
                ft.Container(
                    content=boton_check,
                    width=50,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color="#c62828",
                        tooltip="Eliminar sugerencia",
                        on_click=lambda e: eliminar(sugerencia.id_sugerencia)
                    ),
                    width=50,
                    alignment=ft.alignment.center
                )
            ])
        )
        return fila

    def actualizar_tabla():
        tabla.controls.clear()
        sugerencias = obtener_sugerencias()
        for s in sugerencias:
            tabla.controls.append(crear_fila(s))
        page.update()

    encabezado = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text("Fecha", weight=ft.FontWeight.BOLD, color="#ffffff"),
                width=120,
                padding=10,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Text("Producto", weight=ft.FontWeight.BOLD, color="#ffffff"),
                width=200,
                padding=10,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Text("Comentario", weight=ft.FontWeight.BOLD, color="#ffffff"),
                width=300,
                padding=10,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Text("Acciones", weight=ft.FontWeight.BOLD, color="#ffffff"),
                width=100,
                padding=10,
                alignment=ft.alignment.center
            ),
        ]),
        bgcolor="#1da3c2",
        border_radius=8,
        margin=ft.margin.only(bottom=10)
    )

    actualizar_tabla()

    return ft.Container(
        content=ft.Column([
            ft.Text(
                "Sugerencias de Clientes",
                size=24,
                weight=ft.FontWeight.BOLD,
                color="#090040",
                text_align=ft.TextAlign.CENTER,
                style=ft.TextThemeStyle.HEADLINE_MEDIUM
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            encabezado,
            ft.Container(
                content=tabla,
                expand=True,
                padding=ft.padding.symmetric(horizontal=10)
            ),
        ],
        expand=True,
        spacing=0
        ),
        padding=20,
        expand=True,
        bgcolor="#f2f7fb"
    )

def main(page: ft.Page):
    page.title = "Sugerencias de clientes"
    page.bgcolor = "#f2f7fb"
    page.views.clear()
    page.views.append(
        ft.View(
            route="/sugerencias",
            controls=[sugerencias_view(page)],
            bgcolor="#f2f7fb",
            padding=0
        )
    )
    page.update()

ft.app(target=main)
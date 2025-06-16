import flet as ft

from papeleria_app.models.sugerencia_cliente import SugerenciaCliente
from papeleria_app.repositorios.sugerencia_repo import obtener_sugerencias, eliminar_sugerencia

# Diccionario que guarda el estado visual de las sugerencias marcadas como realizadas
estado_realizadas = {}

def sugerencias_view(page: ft.Page):
    tabla = ft.Column()

    def marcar_como_realizada(id_sugerencia):
        estado_realizadas[id_sugerencia] = True
        actualizar_tabla()

    def eliminar(id_sugerencia):
        eliminar_sugerencia(id_sugerencia)
        estado_realizadas.pop(id_sugerencia, None)
        actualizar_tabla()

    def crear_fila(sugerencia: SugerenciaCliente):
        realizada = estado_realizadas.get(sugerencia.id_sugerencia, False)
        fila_color = "#dcedc8" if realizada else "#e8f5e9"

        boton_check = ft.IconButton(
            icon=ft.Icons.CHECK,
            icon_color="green",
            tooltip="Marcar como realizada",
            visible=not realizada,
            on_click=lambda e: marcar_como_realizada(sugerencia.id_sugerencia)
        )

        fila = ft.Container(
            bgcolor=fila_color,
            padding=10,
            border_radius=5,
            content=ft.Row([
                ft.Container(ft.Text(sugerencia.fecha_sugerencia.strftime("%Y-%m-%d")), width=120),
                ft.Container(ft.Text(sugerencia.producto_sugerido), width=200),
                ft.Container(ft.Text(sugerencia.comentario), width=300),
                boton_check,
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color="red",
                    tooltip="Eliminar sugerencia",
                    on_click=lambda e: eliminar(sugerencia.id_sugerencia)
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

    encabezado = ft.Row([
        ft.Container(ft.Text("Fecha", weight="bold"), bgcolor="#a5d6a7", width=120, padding=10),
        ft.Container(ft.Text("Producto sugerido", weight="bold"), bgcolor="#a5d6a7", width=200, padding=10),
        ft.Container(ft.Text("Comentario", weight="bold"), bgcolor="#a5d6a7", width=300, padding=10),
        ft.Container(ft.Text("✔️"), bgcolor="#a5d6a7", width=50),
        ft.Container(ft.Text("❌"), bgcolor="#a5d6a7", width=50),
    ])

    actualizar_tabla()

    return ft.Column([
        ft.Text("Sugerencias de clientes", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
        encabezado,
        tabla,
    ])

def main(page: ft.Page):
    page.title = "Sugerencias de clientes"
    page.views.clear()
    page.views.append(
        ft.View(route="/sugerencias", controls=[sugerencias_view(page)])
    )
    page.update()

ft.app(target=main)

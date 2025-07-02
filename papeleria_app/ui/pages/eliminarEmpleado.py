import flet as ft
from papeleria_app.repositorios.empleado_repo import obtener_empleados_simulados, eliminar_o_suspender_empleado

def baja_empleado_view(page: ft.Page):
    page.title = "Baja de Empleados"

    mensaje = ft.Text("", size=14, color="red", text_align=ft.TextAlign.CENTER)

    empleados = obtener_empleados_simulados()

    def refrescar_lista():
        controles = []
        for empleado in empleados:
            # Mostramos todos, pero ponemos diferente color si está inactivo
            bg_color = "#e0e0e0" if not empleado.activo else "#007acc"  # gris claro si inactivo, azul si activo
            text_color = "black" if not empleado.activo else "white"

            boton_eliminar = ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color="white",
                bgcolor="red",
                tooltip="Eliminar o suspender empleado",
                on_click=lambda e, nom=empleado.nombre: eliminar_click(nom),
                disabled=not empleado.activo  # Si ya está inactivo, no se puede eliminar otra vez
            )
            controles.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{empleado.nombre} - {empleado.rol} - {'Activo' if empleado.activo else 'Inactivo'}",
                                    color=text_color),
                            boton_eliminar
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=10,
                    bgcolor=bg_color,
                    margin=ft.margin.only(bottom=8),
                    border_radius=8,
                    width=400
                )
            )
        return controles

    def eliminar_click(nombre):
        exito = eliminar_o_suspender_empleado(nombre)
        if exito:
            if nombre == "Juan Pérez":
                mensaje.value = f"Empleado '{nombre}' eliminado correctamente."
            else:
                mensaje.value = f"Empleado '{nombre}' cambiado a inactivo (ventas registradas)."
            mensaje.color = "green"
        else:
            mensaje.value = f"No se pudo eliminar o suspender a '{nombre}'."
            mensaje.color = "red"
        page.update()
        actualizar_lista()

    def actualizar_lista():
        empleados_control.controls.clear()
        empleados_control.controls.extend(refrescar_lista())
        page.update()

    empleados_control = ft.Column(spacing=5)
    actualizar_lista()

    return ft.Column(
        controls=[
            ft.Text("Baja de Empleados", size=24, weight="bold"),
            empleados_control,
            mensaje
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

def main(page: ft.Page):
    page.views.clear()
    page.views.append(ft.View(route="/eliminar_empleado", controls=[baja_empleado_view(page)]))
    page.update()


ft.app(target=main)
import flet as ft
from papeleria_app.repositorios.usuario_repo import obtener_empleados_activos, actualizar_nombre_contrasena

def editar_empleado_view(page: ft.Page):
    empleados_dropdown = ft.Dropdown(label="Seleccionar Empleado", width=300)
    id_input = ft.TextField(label="ID", width=300, disabled=True)
    nombre_input = ft.TextField(label="Nombre", width=300)
    contrasena_input = ft.TextField(label="Nueva Contraseña", width=300, password=True, can_reveal_password=True)
    rol_input = ft.TextField(label="Rol", width=300, disabled=True)
    estado_input = ft.TextField(label="Estado", width=300, disabled=True)
    mensaje = ft.Text("", color="red", size=14)

    empleados_data = obtener_empleados_activos()
    opciones_dropdown = []

    for emp in empleados_data:
        opciones_dropdown.append(ft.dropdown.Option(str(emp.id_usuario)))
    empleados_dropdown.options = opciones_dropdown

    def cargar_datos(e):
        if empleados_dropdown.value:
            seleccionado = next((emp for emp in empleados_data if str(emp.id_usuario) == empleados_dropdown.value), None)
            if seleccionado:
                id_input.value = str(seleccionado.id_usuario)
                nombre_input.value = seleccionado.nombre
                rol_input.value = seleccionado.rol
                estado_input.value = "ACTIVO" if seleccionado.activo else "INACTIVO"
                contrasena_input.value = ""
                mensaje.value = ""
                mensaje.color = "black"
                page.update()

    empleados_dropdown.on_change = cargar_datos

    def guardar_cambios(e):
        if not empleados_dropdown.value:
            mensaje.value = "Selecciona un empleado."
            mensaje.color = "red"
            page.update()
            return

        nuevo_nombre = nombre_input.value.strip()
        nueva_contra = contrasena_input.value.strip()
        id_usuario = int(id_input.value)

        if not nuevo_nombre:
            mensaje.value = "El nombre no puede estar vacío."
            mensaje.color = "red"
            page.update()
            return

        exito, msj = actualizar_nombre_contrasena(id_usuario, nuevo_nombre, nueva_contra if nueva_contra else None)
        mensaje.value = msj
        mensaje.color = "green" if exito else "red"
        page.update()

    layout = ft.Column(
        controls=[
            ft.Text("EDITAR EMPLEADO", size=24, weight="bold"),
            empleados_dropdown,
            id_input,
            nombre_input,
            contrasena_input,
            rol_input,
            estado_input,
            mensaje,
            ft.Row(
                controls=[
                    ft.ElevatedButton("Guardar Cambios", on_click=guardar_cambios),
                    ft.ElevatedButton("Cancelar", on_click=lambda e: page.go("/"))
                ]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    return layout


def main(page: ft.Page):
    page.title = "Editar Empleado"
    page.views.clear()
    page.views.append(
        ft.View(
            route="/editar_empleado",
            controls=[editar_empleado_view(page)],
        )
    )
    page.update()



ft.app(target=main)

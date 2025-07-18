import flet as ft

# Simulación de empleado
class Empleado:
    def _init_(self, id_usuario, nombre, rol, activo=True):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rol = rol
        self.activo = activo

# "Base de datos" en memoria
empleados_db = [
    Empleado(1, "Marlon Morgado", "encargado"),
    Empleado(2, "Ana Escobedo", "empleado"),
    Empleado(3, "Agustín Piñon", "encargado"),
    Empleado(4, "Citlalli Lira", "encargado"),
    Empleado(5, "Juan Pérez", "empleado"),
]

# Empleados no eliminables
NO_ELIMINABLES = {"Marlon Morgado", "Agustín Piñon", "Citlalli Lira", "Ana Escobedo"}

def obtener_empleados_activos():
    return [e for e in empleados_db if e.activo]

def eliminar_o_desactivar_empleado(id_usuario):
    for emp in empleados_db:
        if emp.id_usuario == id_usuario:
            if emp.nombre in NO_ELIMINABLES:
                return False, f"No se puede eliminar a {emp.nombre}: tiene privilegios especiales."
            if emp.nombre == "Juan Pérez":
                empleados_db.remove(emp)
                return True, f"{emp.nombre} eliminado correctamente (sin ventas registradas)."
            else:
                emp.activo = False
                return True, f"{emp.nombre} ha sido dado de baja (inactivo)."
    return False, "Empleado no encontrado."

# Componente de encabezado simulado
class Logo_header:
    def _init_(self, path):
        self.path = path

    def getHeader(self):
        return ft.Container(
            height=100,
            bgcolor="#3b5998",
            alignment=ft.alignment.center,
            content=ft.Text("PAPELERÍA MARLONS", size=30, color="white", weight="bold")
        )

def eliminar_empleado_view(page: ft.Page):
    header = Logo_header("papeleria_app/images/logo_blanco.jpg").getHeader()
    empleados_column = ft.Column(scroll="auto", expand=True)
    mensaje = ft.Text("", size=14, color="green", text_align=ft.TextAlign.CENTER)

    def confirmar_eliminacion(id_usuario):
        def si_confirma(e):
            ok, msg = eliminar_o_desactivar_empleado(id_usuario)
            mensaje.value = msg
            mensaje.color = "green" if ok else "red"
            dialog.open = False
            cargar_empleados()
            page.update()

        def no_confirma(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Estás seguro de que deseas dar de baja a este empleado?"),
            actions=[
                ft.TextButton("CANCELAR", on_click=no_confirma),
                ft.TextButton("BORRAR", on_click=si_confirma)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def crear_boton_eliminar(uid):
        return ft.ElevatedButton(
            "DAR DE BAJA",
            on_click=lambda e: confirmar_eliminacion(uid),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=20,
                bgcolor="#8e9ebc",
            ),
            width=200
        )

    def crear_icono_cancelar(uid):
        return ft.IconButton(
            icon=ft.icons.CANCEL,
            icon_color="white",
            bgcolor="red",
            tooltip="Eliminar empleado",
            on_click=lambda e: confirmar_eliminacion(uid)
        )

    def cargar_empleados():
        empleados_column.controls.clear()
        empleados = obtener_empleados_activos()

        if not empleados:
            empleados_column.controls.append(ft.Text("No hay empleados activos."))
        else:
            for emp in empleados:
                empleados_column.controls.append(
                    ft.Container(
                        bgcolor="#dce1f0",
                        border_radius=20,
                        padding=20,
                        width=500,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Text("BAJA DE EMPLEADOS", size=20, weight="bold"),
                                ft.Row([ft.Text("ID:", weight="bold"), ft.Text(str(emp.id_usuario))]),
                                ft.Row([ft.Text("NOMBRE:", weight="bold"), ft.Text(emp.nombre)]),
                                ft.Row([ft.Text("ROL:", weight="bold"), ft.Text(emp.rol)]),
                                ft.Row([ft.Text("ESTADO:", weight="bold"), ft.Text("ACTIVO")]),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[crear_boton_eliminar(emp.id_usuario)]
                                ),
                                crear_icono_cancelar(emp.id_usuario)
                            ]
                        )
                    )
                )
        page.update()

    cargar_empleados()

    layout = ft.Column(
        expand=True,
        controls=[
            header,
            mensaje,
            ft.Container(
                expand=True,
                alignment=ft.alignment.top_center,
                bgcolor="#ccecf3",
                padding=40,
                content=empleados_column
            )
        ]
    )

    return layout

def main(page: ft.Page):
    page.title = "Eliminar Empleado"
    page.bgcolor = "#cdf3ff"
    page.views.clear()
    page.views.append(
        ft.View(
            route="/eliminar_empleado",
            bgcolor="#cdf3ff",
            padding=0,
            spacing=0,
            controls=[eliminar_empleado_view(page)],
        )
    )
    page.update()

ft.app(target=main)